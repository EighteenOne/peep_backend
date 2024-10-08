import logging
import sys
from os import path

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers.api import router
from app.routers.sentry_webhook import sentry_router
from app.tasks.tasks import create_template, create_point
from app.utils.init_db import create_tables
from app.config.database import get_db

from fastapi_utils.tasks import repeat_every
from app.tasks import tasks

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# stream_handler = logging.StreamHandler(sys.stdout)
# log_formatter = logging.Formatter(
#     "%(asctime)s [%(levelname)s]: %(message)s")
# stream_handler.setFormatter(log_formatter)
# logger.addHandler(stream_handler)

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
    root_path="/peep"
)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="API",
    )


@app.on_event("startup")
def on_startup() -> None:
    # create_tables()
    # create_template()
    # create_point()
    return


@app.on_event("startup")
@repeat_every(seconds=60, logger=logger)
def run_task_check_files_count() -> None:
    tasks.update_uploaded_count_photos(logger)


@app.on_event("startup")
@repeat_every(seconds=70, logger=logger)
def run_task_send_notifications() -> None:
    tasks.send_emails(logger)


origins = ["*"]

# if settings.DEBUG:
#     origins = ["*"]
# else:
#     origins = [
#         str(origin).strip(",") for origin in settings.ORIGINS
#     ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(sentry_router)

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", reload=True)
