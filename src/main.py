import sys
sys.path.append("..")

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.config import settings
from src.api import router


def create_fast_api_app():
    if settings.MODE != 'PROD':
        _app = FastAPI(
            default_response_class=ORJSONResponse,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            docs_url=None,
            redoc_url=None
        )

    _app.include_router(router)

    return _app


app = create_fast_api_app()
