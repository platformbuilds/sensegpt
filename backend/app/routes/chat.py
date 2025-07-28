
from fastapi import APIRouter, Request
import requests
import os
from clickhouse_driver import Client

router = APIRouter()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
client = Client(
    host=os.getenv("CH_DB_HOST", "clickhouse"),
    user=os.getenv("CH_DB_USER", "default"),
    password=os.getenv("CH_DB_PASSWORD", ""),
    database=os.getenv("CH_DB_NAME", "default")
)

PROMPT_TEMPLATE = '''
You are an observability assistant. Based on the user's request, write a SQL query for ClickHouse that returns OpenTelemetry trace information.

Only return the SQL query, no explanation.

User Request:
{question}
'''

@router.post("/chat")
async def chat_query(req: Request):
    data = await req.json()
    question = data.get("prompt", "")

    prompt = PROMPT_TEMPLATE.format(question=question)

    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )

    if res.status_code != 200:
        return {"response": "Failed to connect to LLM backend."}

    response_data = res.json()
    generated_sql = response_data.get("response", "").strip()

    # Try executing generated SQL
    try:
        result = client.execute(generated_sql)
        columns = [desc[0] for desc in client.execute(f"DESCRIBE TABLE otel_traces")]
        return {
            "sql": generated_sql,
            "result": [dict(zip(columns, row)) for row in result]
        }
    except Exception as e:
        return {
            "sql": generated_sql,
            "error": str(e)
        }
