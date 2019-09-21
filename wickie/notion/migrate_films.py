import os
import re
import notion
from notion.client import NotionClient
from notion.block import ImageBlock
import simplejson as json

from wickie.settings import NOTION_PAGE, NOTION_TOKEN
from wickie.notion.multiselect import add_genre, add_creators

# from prepare_films import prepare_films


def add_film(film, collection_view, genre_prop, creators_prop):
    new_film = collection_view.collection.add_row()
    new_film.category = "Film"
    new_film.status = "Not Started"
    new_film.title = film["title"]
    new_film.link = film["link"]
    new_film.year = int(film["date"].strftime("%Y"))
    image = new_film.children.add_new(ImageBlock)
    image.set_source_url(film["poster"])
    add_genre(new_film, film["genre"], genre_prop)
    add_creators(new_film, film["creators"], creators_prop)


# def main():
#     films = prepare_films()
#     notion_client = NotionClient(token_v2=NOTION_TOKEN)
#     collection_view = notion_client.get_collection_view(NOTION_PAGE)
#     genre_prop = collection_view.collection.get_schema_property("genre")
#     creators_prop = collection_view.collection.get_schema_property("creators")
#     for i, film in enumerate(films, start=1):
#         print(
#             "Adding '{}' ({}/{})".format(
#                 film["title"], str(i), str(len(films))
#             )
#         )
#         add_film(film, collection_view, genre_prop, creators_prop)


# main()
