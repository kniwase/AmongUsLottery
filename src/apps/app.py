from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from settings import SCRIPTS_PATH, STYLES_PATH, PAGES_PATH
from router import router_api, router_view


api = FastAPI(
    title="AmongUs特殊配役抽選",
    description="",
    version="0.0.1",
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)

api.include_router(router_view, prefix="/amgus-lot")
api.include_router(router_api, prefix="/amgus-lot/api")
api.mount("/amgus-lot/scripts", StaticFiles(directory=SCRIPTS_PATH))
api.mount("/amgus-lot/styles", StaticFiles(directory=STYLES_PATH))
api.mount("/amgus-lot/pages", StaticFiles(directory=PAGES_PATH))
