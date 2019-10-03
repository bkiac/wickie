import re
import logging

from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from wickie.bot.helpers import (
    logger,
    restricted,
    send_typing_action,
    create_confirmation_keyboard,
    CONFIRMATION_STATE,
    YES,
    NO,
    NEW_PAGE_KEY,
)
from wickie.utils import prettier
from wickie.omdb import client as omdb_client
from wickie.settings import TELEGRAM_BOT_TOKEN
import wickie.notionutils.prepare as prepare_for_notion
from wickie.notionutils.add import add as add_to_notion
import wickie.omdb as omdb
import wickie.goodreads.goodreads as goodreads


@restricted
def handle_start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!")


@restricted
def handle_help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


@restricted
def handle_imdb(update, context):
    """Handle IMDb link."""
    imdb_id = omdb.extract_id(update.message.text)
    film = prepare_for_notion.film(omdb_client.get(imdbid=imdb_id))
    update.message.reply_text(
        prettier(film), reply_markup=create_confirmation_keyboard()
    )
    update.message.reply_text("Looks good? 🔍")
    context.user_data[NEW_PAGE_KEY] = film
    return CONFIRMATION_STATE


@restricted
def handle_goodreads(update, context):
    """Handle Goodreads link."""
    return update.message.reply_text(
        "Goodreads: {}".format(update.message.text)
    )


@restricted
@send_typing_action
def handle_accept(update, context):
    update.message.reply_text("Great! Adding to Notion... 🔦")
    try:
        url = add_to_notion(context.user_data[NEW_PAGE_KEY])
        update.message.reply_text(f"Check out your new page at: {url} 👀")
    except Exception:  # TODO Catch more specific exception
        update.message.reply_text("Something has went wrong! 🤦‍♀️")
    context.user_data.clear()
    return ConversationHandler.END


@restricted
def handle_reject(update, context):
    update.message.reply_text("Sorry. 😔")
    context.user_data.clear()
    return ConversationHandler.END


@restricted
def handle_unknown(update, context):
    update.message.reply_text("Unknown Command")


@restricted
def handle_error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def launch():
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", handle_start))
    dp.add_handler(CommandHandler("help", handle_help))

    ch = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(omdb.r_imdb_url), handle_imdb)
        ],
        states={
            CONFIRMATION_STATE: [
                MessageHandler(Filters.regex(YES), handle_accept),
                MessageHandler(Filters.regex(NO), handle_reject),
            ]
        },
        fallbacks=[MessageHandler(Filters.text, handle_unknown)],
    )
    dp.add_handler(ch)

    dp.add_handler(MessageHandler(Filters.regex(omdb.r_imdb_url), handle_imdb))
    # dp.add_handler(
    #     MessageHandler(
    #         Filters.regex(goodreads.r_goodreads_url), handle_goodreads
    #     )
    # )

    dp.add_handler(MessageHandler(Filters.text, handle_unknown))

    dp.add_error_handler(handle_error)

    updater.start_polling()

    updater.idle()
