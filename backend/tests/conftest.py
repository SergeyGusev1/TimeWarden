import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import Base, get_async_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine):
    session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

    async def override_get_session():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_session

    async with session_maker() as session:
        yield session

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


SAMPLE_ACTIVITY = {
    "app_name": "Visual Studio Code",
    "window_title": "app.py - TimeWarden",
    "category": "productive",
    "duration_seconds": 3600.0,
    "start_time": "2024-01-15T10:00:00",
    "end_time": "2024-01-15T11:00:00",
}
