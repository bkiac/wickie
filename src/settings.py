import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
GOODREADS_API_KEY = os.getenv("GOODREADS_API_KEY")
GOODREADS_API_SECRET = os.getenv("GOODREADS_API_SECRET")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_FILMS_COLLECTION_VIEW = os.getenv("NOTION_FILMS_COLLECTION_VIEW")
NOTION_BOOKS_COLLECTION_VIEW = os.getenv("NOTION_BOOKS_COLLECTION_VIEW")

folder_path = os.path.dirname(os.path.abspath(__file__))

data_folder_path = "data"

books_csv = os.path.join(
    folder_path, *[data_folder_path, "books_from_spreadsheet.csv"]
)
books_json = os.path.join(
    folder_path, *[data_folder_path, "books_scraped_from_goodreads.json"]
)
books_merge_csv = os.path.join(
    folder_path, *[data_folder_path, "books_merge.csv"]
)

films_csv = os.path.join(
    folder_path, *[data_folder_path, "films_from_todoist.csv"]
)
films_json = os.path.join(
    folder_path, *[data_folder_path, "films_from_omdb.json"]
)
films_merge_csv = os.path.join(
    folder_path, *[data_folder_path, "films_merge.csv"]
)
