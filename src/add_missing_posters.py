import os
import re
import notion
from notion.client import NotionClient
from notion.block import ImageBlock
import simplejson as json

from settings import (
    NOTION_FILMS_COLLECTION_VIEW,
    NOTION_BOOKS_COLLECTION_VIEW,
    NOTION_TOKEN,
)
from multiselect import add_genre, add_creators
from prepare import prepare_films_for_api, prepare_books_for_api


def find_item(items, name):
    return next((i for i in items if i["Name"] == name), None)


def add_poster(page, item):
    print('Adding poster for "{}"'.format(page.name))
    image = page.children.add_new(ImageBlock)
    image.set_source_url(item["Poster"])


def add_posters(collection_view, items):
    for row in collection_view.default_query().execute():
        print('Reading item "{}"'.format(row.name))
        item = find_item(items, row.name)
        if item is not None:
            add_poster(row, item)


def main():
    notion_client = NotionClient(token_v2=NOTION_TOKEN)
    films_cv = notion_client.get_collection_view(NOTION_FILMS_COLLECTION_VIEW)
    books_cv = notion_client.get_collection_view(NOTION_BOOKS_COLLECTION_VIEW)
    add_posters(films_cv, prepare_films_for_api())
    add_posters(books_cv, prepare_books_for_api())


main()
