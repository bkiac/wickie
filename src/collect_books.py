import os
import csv
import simplejson as json
import requests
import xmltodict
import goodreads
from dateutil.parser import parse as parse_date
from datetime import datetime

from settings import (
    GOODREADS_API_KEY,
    GOODREADS_API_SECRET,
    books_csv,
    books_json,
)


def parse_book_row(row):
    return {
        "title": row[1],
        "date_started": row[3],
        "date_finished": row[4],
        "progress": row[5],
        "why": row[7],
        "notes": row[9],
    }


def collect_book(book):
    search_result_title = goodreads.search_book_by_title(book["title"])
    goodreads_book = goodreads.get_book(search_result_title)
    return {**book, **goodreads_book}


def collect_books(books):
    collected_books = []
    for i, b in enumerate(books, start=1):
        time = datetime.now().time().strftime("%H:%M:%S")
        print(
            '[{}] Collecting "{}" ({}/{})'.format(
                time, b["title"], str(i), str(len(books))
            )
        )
        collected_books.append(collect_book(b))
    return collected_books


def main():
    with open(books_csv, newline="") as f:
        reader = csv.reader(f)
        next(reader)

        parsed_books = [parse_book_row(r) for r in reader]
        collected_books = collect_books(parsed_books)

        with open(books_json, "w") as f:
            json.dump(collected_books, f, indent=2)


main()
