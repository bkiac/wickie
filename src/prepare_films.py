import os
import re
import simplejson as json
import datetime

from settings import folder


def parse_date(date_str):
    # e.g.: 30 Jan 2009
    return datetime.datetime.strptime(date_str, "%d %b %Y")


def sanitize_creator(creator):
    return re.sub(r"\([a-zA-Z\s]*\)", "", creator).strip()


def remove_not_available(items):
    return [i for i in items if i != "N/A"]


def prepare_film(film):
    title = film["Title"] + " (" + film["Year"] + ")"
    release_date = parse_date(film["Released"])
    genre = remove_not_available([g.strip() for g in film["Genre"].split(",")])
    directors = [sanitize_creator(d) for d in film["Director"].split(",")]
    writers = [sanitize_creator(w) for w in film["Writer"].split(",")]
    all_creators = remove_not_available(list(set(directors + writers)))
    poster = film["Poster"]
    link = "https://imdb.com/title/" + film["imdbID"]
    return {
        "title": title,
        "release_date": release_date,
        "genre": genre,
        "creators": all_creators,
        "poster": poster,
        "link": link,
    }


def prepare_films():
    films_json = os.path.join(folder, "films.json")
    with open(films_json, "r") as f:
        films = json.load(f)
        prepared_films = [prepare_film(f) for f in films]
        return prepared_films
