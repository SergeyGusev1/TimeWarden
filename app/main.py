from fastapi import FastAPI

from app.core.config import settings
from app.api.v1 import router


app = FastAPI(title=settings.APP_NAME)
app.include_router(router)


@app.get('/')
def root():
    return {'message': 'TimeWarden is alive'}
