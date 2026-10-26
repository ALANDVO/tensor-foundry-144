"""
Tensor Foundry 144 - Backend API
Makes your AI agent think like the laziest senior dev in the room.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ConfigModel(BaseModel):
    default_mode: Optional[str] = None
    hide_status: bool = False
    quiet_startup: bool = False
    map_enabled: bool = True
    map_chars: int = 2000


# In-memory config store (replace with file persistence later)
config_store: ConfigModel = ConfigModel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Tensor Foundry 144 backend starting...")
    yield
    # Shutdown
    print("Tensor Foundry 144 backend shutting down...")


app = FastAPI(
    title="Tensor Foundry 144",
    description="Makes your AI agent think like the laziest senior dev in the room.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        service="tensor-foundry-144",
        version="0.1.0",
    )


@app.get("/api/config", response_model=ConfigModel)
async def get_config():
    """Get current configuration."""
    return config_store


@app.post("/api/config", response_model=ConfigModel)
async def update_config(config: ConfigModel):
    """Update configuration."""
    global config_store
    config_store = config
    return config_store


@app.get("/api/modes")
async def get_modes():
    """Get available modes."""
    return {
        "modes": ["off", "lite", "standard", "ultra"],
        "descriptions": {
            "off": "No Ponytail instructions injected",
            "lite": "Minimal guidance - just the essentials",
            "standard": "Balanced guidance for most tasks",
            "ultra": "Maximum guidance - thorough analysis",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)