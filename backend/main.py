
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze, chat

app = FastAPI(
    title="Sense-MCP",
    version="1.0.0",
    description="MCP Server for OpenTelemetry data in ClickHouse"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/mcp")
app.include_router(chat.router, prefix="/api/mcp")
