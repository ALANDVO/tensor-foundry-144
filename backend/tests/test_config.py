import pytest
from httpx import ASGITransport, AsyncClient
from main import app
import main
import os
import tempfile
from pathlib import Path


@pytest.mark.asyncio
async def test_config_file_persistence():
    """Test that config updates persist to file and survive reload."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_config_path = Path(f.name)
    
    original_config_file = main.CONFIG_FILE
    original_config_store = main.config_store
    
    try:
        main.CONFIG_FILE = temp_config_path
        
        # Reload config from file (empty file should give defaults)
        main.file_config = main.load_config_from_file()
        main.env_settings = main.Settings()
        main.config_store = main.merge_configs(main.file_config, main.env_settings)
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Update config
            new_config = {
                "default_mode": "standard",
                "hide_status": False,
                "quiet_startup": False,
                "map_enabled": True,
                "map_chars": 2500,
            }
            response = await client.post("/api/config", json=new_config)
            assert response.status_code == 200
            
            # Verify file was written
            assert temp_config_path.exists()
            with open(temp_config_path, 'r') as f:
                saved_data = json.load(f)
            assert saved_data["default_mode"] == "standard"
            assert saved_data["map_chars"] == 2500
            
            # Verify subsequent GET returns persisted config
            response = await client.get("/api/config")
            assert response.status_code == 200
            data = response.json()
            assert data["default_mode"] == "standard"
            assert data["map_chars"] == 2500
    finally:
        main.CONFIG_FILE = original_config_file
        main.config_store = original_config_store
        if temp_config_path.exists():
            temp_config_path.unlink()


@pytest.mark.asyncio
async def test_env_var_overrides():
    """Test that environment variables override file config."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_config_path = Path(f.name)
        # Write a config file with specific values
        json.dump({"default_mode": "lite", "map_chars": 1000}, f)
    
    original_config_file = main.CONFIG_FILE
    original_config_store = main.config_store
    original_env = dict(os.environ)
    
    try:
        main.CONFIG_FILE = temp_config_path
        
        # Set environment variables that should override file
        os.environ["PONYTAIL_DEFAULT_MODE"] = "ultra"
        os.environ["PONYTAIL_MAP_CHARS"] = "5000"
        
        # Reload config
        main.file_config = main.load_config_from_file()
        main.env_settings = main.Settings()
        main.config_store = main.merge_configs(main.file_config, main.env_settings)
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/config")
            assert response.status_code == 200
            data = response.json()
            # Env vars should override file
            assert data["default_mode"] == "ultra"
            assert data["map_chars"] == 5000
    finally:
        main.CONFIG_FILE = original_config_file
        main.config_store = original_config_store
        os.environ.clear()
        os.environ.update(original_env)
        if temp_config_path.exists():
            temp_config_path.unlink()


@pytest.mark.asyncio
async def test_mode_validation():
    """Test that invalid modes are rejected."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Valid modes should work
        for mode in ["off", "lite", "standard", "ultra"]:
            response = await client.post("/api/config", json={"default_mode": mode})
            assert response.status_code == 200
            assert response.json()["default_mode"] == mode
        
        # Invalid mode should be rejected
        response = await client.post("/api/config", json={"default_mode": "invalid"})
        assert response.status_code == 422  # Validation error
