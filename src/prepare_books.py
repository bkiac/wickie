import os
import simplejson as json
from dateutil.parser import parse as parse_date

from settings import folder


def prepare_date(date):
    return parse_date(date) if date != "?" and date != "" else None


def prepare_progress(progress):
    progress_map = {
        "": "Not Started",
        "unstarted": "Not Started",
        "current": "Current",
        "finished": "Finished",
        "unfinished": "Abandoned",
    }
    return progress_map[progress]


def prepare_publication_date(publication_date):
    try:
        year = parse_date(publication_date).year
        return year
    except ValueError:
        return int(publication_date)


def prepare_book(book):
    return {
        "title": book["title"],
        "category": "Book",
        "status": prepare_progress(book["progress"]),
        "link": book["url"],
        "year": prepare_publication_date(book["publication_date"]),
        "poster": book["cover_image"],
        "genre": book["genres"],
        "creators": book["authors"],
        "start_date": prepare_date(book["date_started"]),
        "finish_date": prepare_date(book["date_finished"]),
        "why": book["why"],
        "summary": book["notes"],
    }


def prepare_books():
    books_json = os.path.join(folder, "books.json")
    with open(books_json, "r") as f:
        books = json.load(f)
        prepared_books = [prepare_book(b) for b in books]
        return prepared_books
