import os
import re
import notion
from notion.client import NotionClient
from notion.block import ImageBlock
import simplejson as json

import settings
from prepare_films import prepare_films


def add_multiselect_prop(
    film_page, prop, prop_fallback, new_options, schema_prop
):
    new_options_set = set(new_options)
    current_options_set = set([o["value"] for o in schema_prop["options"]])
    intersection = new_options_set.intersection(current_options_set)
    film_page.set_property(prop, list(intersection))
    if len(new_options_set) > len(intersection):
        difference = [g for g in new_options_set if g not in intersection]
        film_page.set_property(prop_fallback, ",".join(difference))
        # Set `TBP` flag to `True` if it requires manual help
        film_page.tbp = True


def add_genre(film_page, genre, collection_view):
    add_multiselect_prop(
        film_page, "Genre", "Genre String", genre, collection_view
    )


def add_creators(film_page, creators, collection_view):
    add_multiselect_prop(
        film_page, "Creators", "Creators String", creators, collection_view
    )


def add_film(film, collection_view, genre_prop, creators_prop):
    new_film = collection_view.collection.add_row()
    new_film.category = "Film"
    new_film.status = "Unstarted"
    new_film.title = film["title"]
    new_film.link = film["link"]
    new_film.release_date = film["release_date"]
    image = new_film.children.add_new(ImageBlock)
    image.set_source_url(film["poster"])
    add_genre(new_film, film["genre"], genre_prop)
    add_creators(new_film, film["creators"], creators_prop)


def main():
    TOKEN = os.getenv("TOKEN")
    PAGE = os.getenv("PAGE")
    films = prepare_films()
    notion_client = NotionClient(token_v2=TOKEN)
    collection_view = notion_client.get_collection_view(PAGE)
    genre_prop = collection_view.collection.get_schema_property("genre")
    creators_prop = collection_view.collection.get_schema_property("creators")
    for i, film in enumerate(films, start=1):
        print(
            "Adding '"
            + film["title"]
            + "' ("
            + str(i)
            + "/"
            + str(len(films))
            + ")"
        )
        add_film(film, collection_view, genre_prop, creators_prop)


main()
