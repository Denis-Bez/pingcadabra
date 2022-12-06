import pytz

from telegram.ext import ApplicationBuilder, Defaults, PicklePersistence

from settings.config import TOKEN_BOT


# --- Build bot application ---
persistence = PicklePersistence(filepath="model/bot_cash")

defaults = Defaults(tzinfo=pytz.timezone('Asia/Yekaterinburg'))

application = (
    ApplicationBuilder()
    .token(TOKEN_BOT)
    .defaults(defaults)
    .persistence(persistence)
    .build()
)

