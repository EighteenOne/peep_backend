import logging

import telegram
from fastapi import APIRouter, Request

from app.config.settings import settings

logger = logging.getLogger(__name__)

sentry_router = APIRouter(
    prefix="/sentry",
    tags=["sentry"]
)

CHAT_ID = -4570888418


@sentry_router.post("", status_code=200)
async def sentry_handler(
        request: Request
):
    payload = await request.json()

    logger.info(payload)

    tg_msg = f'<b>[{payload["project_name"]}]</b>\n<code>{payload["culprit"]}</code>\n<pre>{payload["message"]}</pre>\n\n{payload["url"]}'

    await send_message_to_chat(tg_msg)

    return "ok"


async def send_message_to_chat(msg: str):
    bot = telegram.Bot(token=settings.BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="html")
