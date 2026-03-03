from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.core.config import settings
from app.api.v1 import router as v1_router
from app.services.scheduler import Scheduler

scheduler = Scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(scheduler.start())
    yield
    scheduler.stop()

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "TimeWarden is alive"}
