import re
import logging
import traceback

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
import wickie.goodreads as goodreads


@restricted
def handle_start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!")


@restricted
def handle_help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def handle_potential_page(page, update, context):
    """Handle common operations for IMDb and Goodreads handlers."""
    update.message.reply_text(
        prettier(page), reply_markup=create_confirmation_keyboard()
    )
    update.message.reply_text("Looks good? 🔍")
    context.user_data[NEW_PAGE_KEY] = page
    return CONFIRMATION_STATE


@restricted
@send_typing_action
def handle_imdb(update, context):
    """Handle IMDb URL."""
    imdb_id = omdb.extract_id(update.message.text)
    film = prepare_for_notion.film(omdb_client.get(imdbid=imdb_id))
    return handle_potential_page(film, update, context)


@restricted
@send_typing_action
def handle_goodreads(update, context):
    """Handle Goodreads URL."""
    book = prepare_for_notion.book(goodreads.get(update.message.text))
    return handle_potential_page(book, update, context)


@restricted
@send_typing_action
def handle_accept(update, context):
    update.message.reply_text("Great! Adding to Notion... 🔦")
    try:
        url = add_to_notion(context.user_data[NEW_PAGE_KEY])
        update.message.reply_text(f"Check out your new page at: {url} 👀")
    except Exception:  # TODO Catch more specific exception
        update.message.reply_text("Something has went wrong! 🤦‍♀️")
        traceback.print_exc()
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
    traceback.print_exc()


def launch():
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", handle_start))
    dp.add_handler(CommandHandler("help", handle_help))

    ch = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(omdb.r_imdb_url), handle_imdb),
            MessageHandler(
                Filters.regex(goodreads.r_goodreads_url), handle_goodreads
            ),
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

    dp.add_handler(MessageHandler(Filters.text, handle_unknown))
    dp.add_error_handler(handle_error)

    updater.start_polling()

    updater.idle()
