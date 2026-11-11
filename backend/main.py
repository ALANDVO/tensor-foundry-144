"""
Tensor Foundry 144 - Backend API
Makes your AI agent think like the laziest senior dev in the room.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
import json
from pathlib import Path


CONFIG_FILE = Path(os.environ.get("PONYTAIL_CONFIG_FILE", "config.json"))


class Settings(BaseSettings):
    """Settings loaded from environment variables."""
    model_config = SettingsConfigDict(env_prefix="PONYTAIL_", case_sensitive=False)

    default_mode: Optional[str] = None
    hide_status: bool = False
    quiet_startup: bool = False
    map_enabled: bool = True
    map_chars: int = 2000


class ConfigModel(BaseModel):
    default_mode: Optional[str] = Field(default=None, pattern="^(off|lite|standard|ultra)?$")
    hide_status: bool = False
    quiet_startup: bool = False
    map_enabled: bool = True
    map_chars: int = Field(default=2000, ge=100, le=100000)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


def load_config_from_file() -> ConfigModel:
    """Load configuration from JSON file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return ConfigModel(**data)
        except (json.JSONDecodeError, OSError, ValueError):
            pass
    return ConfigModel()


def save_config_to_file(config: ConfigModel) -> None:
    """Save configuration to JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config.model_dump(), f, indent=2)
    except OSError:
        pass  # Fail silently for now


def merge_configs(file_config: ConfigModel, env_settings: Settings) -> ConfigModel:
    """Merge file config with environment variable overrides."""
    data = file_config.model_dump()
    env_data = env_settings.model_dump(exclude_unset=True)
    # Environment variables override file config
    for key, value in env_data.items():
        if value is not None:
            data[key] = value
    return ConfigModel(**data)


# Initialize config store with file + env
env_settings = Settings()
file_config = load_config_from_file()
config_store: ConfigModel = merge_configs(file_config, env_settings)


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
    """Update configuration and persist to file."""
    global config_store
    config_store = config
    save_config_to_file(config_store)
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
