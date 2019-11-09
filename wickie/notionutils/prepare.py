import os
import re
from enum import Enum

from dateutil.parser import parse as parse_date


props = {
    "name": "Name",
    "cover": "Cover",
    "status": "Status",
    "category": "Category",
    "link": "Link",
    "authors": "Authors",
    "creators": "Creators",
    "directors": "Directors",
    "writers": "Writers",
    "actors": "Actors",
    "why": "Why",
    "tags": "Tags",
    "genres": "Genres",
    "date": "Date",
    "year": "Year",
    "publisher": "Publisher",
    "start_date": "Start Date",
    "finish_date": "Finish Date",
    "score": "Score",
    "summary": "Summary",
}


def _publication_date(publication_date):
    try:
        year = parse_date(publication_date).year
        return year
    except ValueError:
        return int(publication_date)


def _genres(genres):
    return [g.strip() for g in genres.split(",")]


def _celebrity(celebrity):
    return re.sub(r"\(.*\)", "", celebrity).strip()


def _celebrities(cast):
    return list(set([_celebrity(c) for c in cast.split(",")]))


def book(scraped_book):
    name = (props["name"], scraped_book["title"])
    category = (props["category"], "Book")
    status = (props["status"], "Not Started")
    link = (props["link"], scraped_book["url"])
    year = (props["year"], _publication_date(scraped_book["publication_date"]))
    cover = (props["cover"], scraped_book["cover_image"])
    genres = (props["genres"], scraped_book["genres"])
    authors = (props["authors"], scraped_book["authors"])
    return dict([name, category, status, link, year, cover, genres, authors])


def _omdb_common(omdb_response):
    name = (props["name"], omdb_response["title"])
    status = (props["status"], "Not Started")
    link = (
        props["link"],
        f'https://imdb.com/title/{omdb_response["imdb_id"]}',
    )
    date = (props["date"], parse_date(omdb_response["released"]))
    year = (props["year"], int(date[1].year))
    cover = (props["cover"], omdb_response["poster"])
    genres = (props["genres"], _genres(omdb_response["genre"]))
    actors = (props["actors"], _celebrities(omdb_response["actors"]))
    return [name, status, link, year, cover, genres, date, actors]


def film(omdb_film):
    category = (props["category"], "Film")
    directors = (props["directors"], _celebrities(omdb_film["director"]))
    writers = (props["writers"], _celebrities(omdb_film["writer"]))
    return dict(_omdb_common(omdb_film) + [category, directors, writers])


def series(omdb_series):
    category = (props["category"], "Series")
    creators = (props["creators"], _celebrities(omdb_series["writer"]))
    return dict(_omdb_common(omdb_series) + [category, creators])
