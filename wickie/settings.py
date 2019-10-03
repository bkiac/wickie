import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
GOODREADS_API_KEY = os.getenv("GOODREADS_API_KEY")
GOODREADS_API_SECRET = os.getenv("GOODREADS_API_SECRET")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE = os.getenv("NOTION_PAGE")
