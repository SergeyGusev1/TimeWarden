import pytest
from httpx import AsyncClient
from tests.conftest import SAMPLE_ACTIVITY


async def _seed(client: AsyncClient, overrides: dict = None):
    """Создать тестовую активность."""
    payload = {**SAMPLE_ACTIVITY, **(overrides or {})}
    r = await client.post("/api/v1/activity", json=payload)
    assert r.status_code == 200
    return r.json()


@pytest.mark.asyncio
async def test_category_stats_empty(client: AsyncClient):
    response = await client.get("/api/v1/stats/categories")
    assert response.status_code == 200
    data = response.json()
    assert data["total_seconds"] == 0.0
    assert data["categories"] == {}


@pytest.mark.asyncio
async def test_category_stats_with_data(client: AsyncClient):
    await _seed(client)  # productive, 3600s
    await _seed(client, {"category": "wasteful", "duration_seconds": 1800.0})

    response = await client.get("/api/v1/stats/categories")
    assert response.status_code == 200
    data = response.json()

    assert data["total_seconds"] == pytest.approx(5400.0)
    assert "productive" in data["categories"]
    assert "wasteful" in data["categories"]
    assert data["categories"]["productive"]["seconds"] == pytest.approx(3600.0)
    assert data["categories"]["productive"]["percentage"] == pytest.approx(66.7, abs=0.5)


@pytest.mark.asyncio
async def test_daily_stats_empty(client: AsyncClient):
    response = await client.get("/api/v1/stats/daily?days=7")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_daily_stats_with_data(client: AsyncClient):
    await _seed(client)

    response = await client.get("/api/v1/stats/daily?days=30")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Должен быть хотя бы один день
    assert len(data) >= 1
    day = data[0]
    assert "date" in day
    assert "categories" in day


@pytest.mark.asyncio
async def test_daily_stats_days_validation(client: AsyncClient):
    bad = await client.get("/api/v1/stats/daily?days=0")
    assert bad.status_code == 422

    also_bad = await client.get("/api/v1/stats/daily?days=31")
    assert also_bad.status_code == 422


@pytest.mark.asyncio
async def test_top_apps_empty(client: AsyncClient):
    response = await client.get("/api/v1/stats/top-apps")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_top_apps_with_data(client: AsyncClient):
    await _seed(client, {"app_name": "Chrome",  "duration_seconds": 7200.0})
    await _seed(client, {"app_name": "PyCharm", "duration_seconds": 3600.0})
    await _seed(client, {"app_name": "Chrome",  "duration_seconds": 1800.0})

    response = await client.get("/api/v1/stats/top-apps?limit=5")
    assert response.status_code == 200
    data = response.json()

    names = [item["app_name"] for item in data]
    assert "Chrome" in names
    assert "PyCharm" in names

    chrome = next(x for x in data if x["app_name"] == "Chrome")
    assert chrome["total_seconds"] == pytest.approx(9000.0)
    assert chrome["sessions"] == 2


@pytest.mark.asyncio
async def test_top_apps_limit(client: AsyncClient):
    for i in range(5):
        await _seed(client, {"app_name": f"App{i}", "duration_seconds": float(1000 + i)})

    response = await client.get("/api/v1/stats/top-apps?limit=3")
    assert response.status_code == 200
    assert len(response.json()) <= 3


@pytest.mark.asyncio
async def test_top_apps_category_filter(client: AsyncClient):
    await _seed(client, {"app_name": "VSCode",  "category": "productive"})
    await _seed(client, {"app_name": "YouTube", "category": "wasteful"})

    response = await client.get("/api/v1/stats/top-apps?category=productive")
    assert response.status_code == 200
    data = response.json()
    names = [x["app_name"] for x in data]
    assert "VSCode" in names
    assert "YouTube" not in names
