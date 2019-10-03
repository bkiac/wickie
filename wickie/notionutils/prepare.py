import os
import re
from enum import Enum

import simplejson as json
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


def film(omdb_film):
    name = (props["name"], omdb_film["title"])
    category = (props["category"], "Film")
    status = (props["status"], "Not Started")
    link = (props["link"], f'https://imdb.com/title/{omdb_film["imdb_id"]}')
    year = (props["year"], int(omdb_film["year"]))
    cover = (props["cover"], omdb_film["poster"])
    genres = (props["genres"], _genres(omdb_film["genre"]))
    date = (props["date"], parse_date(omdb_film["released"]))
    directors = (props["directors"], _celebrities(omdb_film["director"]))
    writers = (props["writers"], _celebrities(omdb_film["writer"]))
    actors = (props["actors"], _celebrities(omdb_film["actors"]))
    return dict(
        [
            name,
            category,
            status,
            link,
            year,
            cover,
            genres,
            date,
            directors,
            writers,
            actors,
        ]
    )
