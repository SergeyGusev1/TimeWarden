from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.active_endpoints import router as activity_router


app = FastAPI(title=settings.APP_NAME)
app.include_router(activity_router, prefix='/api/v1', tags=['Activities'])


@app.get('/')
def root():
    return {'message': 'TimeWarden is alive'}
