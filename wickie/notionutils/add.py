import os
from uuid import uuid1
from random import choice
from pprint import pprint

from notion.client import NotionClient
from notion.block import ImageBlock

from wickie.settings import NOTION_PAGE, NOTION_TOKEN

notion_client = NotionClient(token_v2=NOTION_TOKEN)
collection_view = notion_client.get_collection_view(NOTION_PAGE)
collection = collection_view.collection
schema = collection.get("schema")

colors = [
    "default",
    "gray",
    "brown",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "red",
]


def _find_prop_schema(prop):
    return next((v for k, v in schema.items() if v["name"] == prop), None)


def _add_new_multi_select_value(prop, value, color=None):
    if color is None:
        color = choice(colors)

    prop_schema = _find_prop_schema(prop)
    if not prop_schema:
        raise ValueError(
            f'"{prop}" property does not exist on the collection!'
        )
    if prop_schema["type"] != "multi_select":
        raise ValueError(f'"{prop}" is not a multi select property!')

    dupe = next(
        (o for o in prop_schema["options"] if o["value"] == value), None
    )
    if dupe:
        raise ValueError(f'"{value}" already exists in the schema!')

    prop_schema["options"].append(
        {"id": str(uuid1()), "value": value, "color": color}
    )
    collection.set("schema", schema)


def _set_multi_select_property(page, prop, new_values):
    new_values_set = set(new_values)
    current_options_set = set(
        [o["value"] for o in _find_prop_schema(prop)["options"]]
    )
    intersection = new_values_set.intersection(current_options_set)
    if len(new_values_set) > len(intersection):
        difference = [g for g in new_values_set if g not in intersection]
        for d in difference:
            _add_new_multi_select_value(prop, d)
    page.set_property(prop, new_values)


def _set_content_cover(block, src):
    image = block.children.add_new(ImageBlock)
    image.set_source_url(src)


def add(prepared_dict):
    new_block = collection_view.collection.add_row()

    if "Cover" in prepared_dict:
        _set_content_cover(new_block, prepared_dict["Cover"])
        prepared_dict.pop("Cover")

    for prop, value in prepared_dict.items():
        if isinstance(value, list):
            _set_multi_select_property(new_block, prop, value)
        else:
            new_block.set_property(prop, value)

    return new_block.get_browseable_url()
