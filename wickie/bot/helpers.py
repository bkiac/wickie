import logging
from functools import wraps

from telegram import ReplyKeyboardMarkup, ChatAction

from wickie.settings import TELEGRAM_USER_ID


CONFIRMATION_STATE = 0

YES = "Yes 👍"
NO = "No 😢"

NEW_PAGE_KEY = 0

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def restricted(func):
    """Restrict usage of func to authorized users only"""

    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != TELEGRAM_USER_ID:
            logger.warning(
                "Unauthorized access denied for {}.".format(user_id)
            )
            return update.message.reply_text("Unauthorized user.")
        return func(update, context, *args, **kwargs)

    return wrapped


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


def create_confirmation_keyboard():
    return ReplyKeyboardMarkup([[YES, NO]], one_time_keyboard=True)
