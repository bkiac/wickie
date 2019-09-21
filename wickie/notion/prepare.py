import os
import simplejson as json
import re
from dateutil.parser import parse as parse_date


def prepare_date(date):
    return parse_date(date) if date != "?" and date != "" else None


def join_list(list):
    return ",".join(list)


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
        "Name": book["title"],
        "Category": "Book",
        "Status": prepare_progress(book["progress"]),
        "Link": book["url"],
        "Year": prepare_publication_date(book["publication_date"]),
        "Poster": book["cover_image"],
        "Genres": book["genres"],
        "Authors": book["authors"],
        "Start Date": prepare_date(book["date_started"]),
        "Finish Date": prepare_date(book["date_finished"]),
        "Why": book["why"],
        "Summary": book["notes"],
    }


def prepare_book_for_merge(book):
    pb = prepare_book(book)
    pb.pop("Poster")
    return {
        **pb,
        "Genres": join_list(pb["Genres"]),
        "Authors": join_list(pb["Authors"]),
    }


def prepare_book_for_api(book):
    return prepare_book(book)


# def prepare_items(json_file, prepare):
#     with open(json_file, "r") as f:
#         return [prepare(i) for i in json.load(f)]


# def prepare_books_for_api():
#     return prepare_items(books_json, prepare_book_for_api)


# def prepare_books_for_merge():
#     return prepare_items(books_json, prepare_book_for_merge)


def sanitize_creator(creator):
    return re.sub(r"\(.*\)", "", creator).strip()


def prepare_film_genres(genres):
    return [g.strip() for g in genres.split(",")]


def prepare_film_cast(cast):
    return list(set([sanitize_creator(c) for c in cast.split(",")]))


def prepare_film(film):
    return {
        "Category": "Film",
        "Status": "Not Started",
        "Name": film["Title"],
        "Date": parse_date(film["Released"]),
        "Genres": prepare_film_genres(film["Genre"]),
        "Directors": prepare_film_cast(film["Director"]),
        "Writers": prepare_film_cast(film["Writer"]),
        "Actors": prepare_film_cast(film["Actors"]),
        "Year": int(film["Year"]),
        "Poster": film["Poster"],
        "Link": "https://imdb.com/title/" + film["imdbID"],
    }


def prepare_film_for_api(film):
    return prepare_film(film)


def prepare_film_for_merge(film):
    pf = prepare_film(film)
    pf.pop("Poster")
    return {
        **pf,
        "Genres": join_list(pf["Genres"]),
        "Directors": join_list(pf["Directors"]),
        "Writers": join_list(pf["Writers"]),
        "Actors": join_list(pf["Actors"]),
    }


# def prepare_films_for_api():
#     return prepare_items(films_json, prepare_film_for_api)


# def prepare_films_for_merge():
#     return prepare_items(films_json, prepare_film_for_merge)
