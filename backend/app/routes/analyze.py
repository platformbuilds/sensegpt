
from fastapi import APIRouter
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os
from clickhouse_driver import Client

router = APIRouter()

# Load model
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/model.pkl")
model = joblib.load(MODEL_PATH)

# ClickHouse client
client = Client(
    host=os.getenv("CH_DB_HOST", "clickhouse"),
    user=os.getenv("CH_DB_USER", "default"),
    password=os.getenv("CH_DB_PASSWORD", ""),
    database=os.getenv("CH_DB_NAME", "default")
)

@router.get("/analyze")
def analyze():
    # Sample query (adjust based on your schema)
    query = """
    SELECT
        trace_id,
        service_name,
        operation_name,
        duration
    FROM otel_traces
    LIMIT 1000
    """
    data = client.execute(query)
    df = pd.DataFrame(data, columns=["trace_id", "service_name", "operation_name", "duration"])

    # Simple feature engineering
    features = pd.get_dummies(df[["service_name", "operation_name"]])
    features["duration"] = df["duration"]

    preds = model.predict(features)
    df["anomaly"] = preds

    return df[df["anomaly"] == -1].to_dict(orient="records")
