import pytest
from httpx import AsyncClient
from tests.conftest import SAMPLE_ACTIVITY


@pytest.mark.asyncio
async def test_create_activity(client: AsyncClient):
    response = await client.post("/api/v1/activity", json=SAMPLE_ACTIVITY)
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == SAMPLE_ACTIVITY["app_name"]
    assert data["category"] == SAMPLE_ACTIVITY["category"]
    assert data["duration_seconds"] == SAMPLE_ACTIVITY["duration_seconds"]
    assert "id" in data


@pytest.mark.asyncio
async def test_create_activity_defaults_category(client: AsyncClient):
    payload = {**SAMPLE_ACTIVITY, "category": "unknown"}
    response = await client.post("/api/v1/activity", json=payload)
    assert response.status_code == 200
    assert response.json()["category"] == "unknown"


@pytest.mark.asyncio
async def test_get_activity_by_id(client: AsyncClient):
    create = await client.post("/api/v1/activity", json=SAMPLE_ACTIVITY)
    activity_id = create.json()["id"]

    response = await client.get(f"/api/v1/activity/{activity_id}")
    assert response.status_code == 200
    assert response.json()["id"] == activity_id


@pytest.mark.asyncio
async def test_get_activity_not_found(client: AsyncClient):
    response = await client.get("/api/v1/activity/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_activities_empty(client: AsyncClient):
    response = await client.get("/api/v1/activity")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_list_activities_pagination(client: AsyncClient):
    # Создаём 5 записей
    for i in range(5):
        payload = {**SAMPLE_ACTIVITY, "app_name": f"App{i}"}
        await client.post("/api/v1/activity", json=payload)

    response = await client.get("/api/v1/activity?page=1&size=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["size"] == 3

    page2 = await client.get("/api/v1/activity?page=2&size=3")
    assert len(page2.json()["items"]) == 2


@pytest.mark.asyncio
async def test_list_activities_invalid_page(client: AsyncClient):
    response = await client.get("/api/v1/activity?page=0")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_activity_invalid_category(client: AsyncClient):
    payload = {**SAMPLE_ACTIVITY, "category": "invalid_category"}
    response = await client.post("/api/v1/activity", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_activity_missing_fields(client: AsyncClient):
    response = await client.post("/api/v1/activity", json={"app_name": "Test"})
    assert response.status_code == 422
