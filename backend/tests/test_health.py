"""Tests for health check endpoint."""
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint returns ok."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "tensor-foundry-144"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_get_config(client: AsyncClient):
    """Test get config endpoint."""
    response = await client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "default_mode" in data
    assert "hide_status" in data
    assert "quiet_startup" in data
    assert "map_enabled" in data
    assert "map_chars" in data


@pytest.mark.asyncio
async def test_update_config(client: AsyncClient):
    """Test update config endpoint."""
    new_config = {
        "default_mode": "lite",
        "hide_status": True,
        "quiet_startup": False,
        "map_enabled": True,
        "map_chars": 1000,
    }
    response = await client.post("/api/config", json=new_config)
    assert response.status_code == 200
    data = response.json()
    assert data["default_mode"] == "lite"
    assert data["hide_status"] is True
    assert data["map_chars"] == 1000


@pytest.mark.asyncio
async def test_get_modes(client: AsyncClient):
    """Test get modes endpoint."""
    response = await client.get("/api/modes")
    assert response.status_code == 200
    data = response.json()
    assert "modes" in data
    assert "descriptions" in data
    assert set(data["modes"]) == {"off", "lite", "standard", "ultra"}