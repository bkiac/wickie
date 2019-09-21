import os
import re
import notion
from notion.client import NotionClient
from notion.block import ImageBlock
import simplejson as json

from wickie.settings import NOTION_PAGE, NOTION_TOKEN
from wickie.notion.multiselect import add_genre, add_creators

# from wickie.notion.prepare import prepare_books


def add_book(book, collection_view, genre_prop, creators_prop):
    new_book = collection_view.collection.add_row()
    new_book.title = book["title"]
    new_book.category = book["category"]
    new_book.status = book["status"]
    new_book.link = book["link"]
    new_book.year = book["year"]
    image = new_book.children.add_new(ImageBlock)
    image.set_source_url(book["poster"])
    add_genre(new_book, book["genre"], genre_prop)
    add_creators(new_book, book["creators"], creators_prop)
    new_book.start_date = book["start_date"]
    new_book.finish_date = book["finish_date"]
    new_book.why = book["why"]
    new_book.summary = book["summary"]


# def main():
#     books = prepare_books()
#     notion_client = NotionClient(token_v2=NOTION_TOKEN)
#     collection_view = notion_client.get_collection_view(NOTION_PAGE)
#     genre_prop = collection_view.collection.get_schema_property("genre")
#     creators_prop = collection_view.collection.get_schema_property("creators")
#     for i, book in enumerate(books, start=1):
#         print(
#             "Adding '{}' ({}/{})".format(
#                 book["title"], str(i), str(len(books))
#             )
#         )
#         add_book(book, collection_view, genre_prop, creators_prop)


# main()
