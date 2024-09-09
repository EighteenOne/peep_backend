import logging
import sys

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers.api import router
from app.tasks.tasks import create_template, create_point
from app.utils.init_db import create_tables
from app.config.database import get_db

from fastapi_utils.tasks import repeat_every
from app.tasks import tasks

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s]: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

app = FastAPI(
    debug=bool(settings.DEBUG),
    title=settings.TITLE,
    root_path="/api/",
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

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", reload=True)
