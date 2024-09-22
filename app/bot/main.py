import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.config.database import SessionLocal
from app.config.settings import settings
from app.repositories.points import PointRepository
from app.services.template import TemplateService

import sentry_sdk

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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

AUTH_LOGIN, AUTH_PASS, CHOOSING, TEMPLATE, STAT = range(5)

choosing_reply_keyboard = [["Шаблон", "Статистика"], ["Сменить точку"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Я Peep-бот, введи название точки",
        reply_markup=ReplyKeyboardRemove(),
    )

    return AUTH_LOGIN


async def start_from_any_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Я Peep-бот, введи название точки",
        reply_markup=ReplyKeyboardRemove(),
    )

    return AUTH_LOGIN


async def auth_login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["point"] = text

    await update.message.reply_text(
        "Введи ключевую фразу",
        reply_markup=ReplyKeyboardRemove(),
    )

    return AUTH_PASS


async def auth_pass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["pass"] = text

    point = context.user_data["point"]
    passw = context.user_data["pass"]

    db = SessionLocal()
    point_repository = PointRepository(db)
    point = point_repository.get_by_point(point=point)
    db.close()

    if point is not None and point.key == passw:
        await update.message.reply_text(
            "Выбери, что нужно сделать",
            reply_markup=ReplyKeyboardMarkup(
                choosing_reply_keyboard, one_time_keyboard=True
            ),
        )
        return CHOOSING

    await update.message.reply_text(
        "Что-то пошло не так. Неверная точка или пароль. Попробуй еще раз - введи название точки",
        reply_markup=ReplyKeyboardRemove(),
    )
    return AUTH_LOGIN


async def change_point(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    del context.user_data["point"]
    del context.user_data["pass"]

    await update.message.reply_text(
        "Введи название точки",
        reply_markup=ReplyKeyboardRemove(),
    )

    return AUTH_LOGIN


async def template_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    point = context.user_data["point"]
    db = SessionLocal()
    template_service = TemplateService(db)
    template = template_service.get_by_point(point)
    db.close()

    await update.message.reply_text(
        "Вот краткая инструкция, как изменить шаблон письма:\n"
        "Отдельным сообщением я пришлю текущий текст шаблона\n"
        "Переменные [Имя] и [Ссылка] будут заменяться на реальные данные при отправке письма\n"
        "В ответном сообщении пришли мне новый текст шаблона и я сразу сохраню его\n\n"
        "А если хочешь отменить редактирование, отправь команду /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )

    await update.message.reply_text(
        "Текущий шаблон:",
        reply_markup=ReplyKeyboardRemove(),
    )

    await update.message.reply_text(
        template.template_text,
        reply_markup=ReplyKeyboardRemove(),
        disable_web_page_preview=True,
    )

    return TEMPLATE


async def change_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    point = context.user_data["point"]

    db = SessionLocal()
    template_service = TemplateService(db)
    template = template_service.get_by_point(point)
    template.template_text = update.message.text
    template_service.update(template)
    db.close()

    await update.message.reply_text(
        "Отлично, я сохранил изменения!",
        reply_markup=ReplyKeyboardMarkup(
            choosing_reply_keyboard, one_time_keyboard=True
        ),
    )

    await update.message.reply_text(
        "Выбери, что нужно сделать",
        reply_markup=ReplyKeyboardMarkup(
            choosing_reply_keyboard, one_time_keyboard=True
        ),
    )

    return CHOOSING


async def stat_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Этот раздел еще в разработке",
        reply_markup=ReplyKeyboardMarkup(
            choosing_reply_keyboard, one_time_keyboard=True
        ),
    )

    return CHOOSING


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Галя, у нас отмена!", reply_markup=ReplyKeyboardMarkup(
            choosing_reply_keyboard, one_time_keyboard=True
        ),
    )

    return CHOOSING


def main() -> None:
    application = Application.builder().token(settings.BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start_from_any_text)
        ],
        states={
            AUTH_LOGIN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, auth_login),
            ],
            AUTH_PASS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, auth_pass),
            ],
            CHOOSING: [
                MessageHandler(filters.Regex("^Шаблон$"), template_choice),
                MessageHandler(filters.Regex("^Статистика$"), stat_choice),
                MessageHandler(filters.Regex("^Сменить точку$"), change_point),
            ],
            TEMPLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_template)],
            # STAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stat)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
