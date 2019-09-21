def add_multiselect_prop(page, prop, prop_fallback, new_options, schema_prop):
    new_options_set = set(new_options)
    current_options_set = set([o["value"] for o in schema_prop["options"]])
    intersection = new_options_set.intersection(current_options_set)
    page.set_property(prop, list(intersection))
    if len(new_options_set) > len(intersection):
        difference = [g for g in new_options_set if g not in intersection]
        page.set_property(prop_fallback, ",".join(difference))


def add_genre(page, genre, collection_view):
    add_multiselect_prop(page, "Genre", "Genre String", genre, collection_view)


def add_creators(page, creators, collection_view):
    add_multiselect_prop(
        page, "Creators", "Creators String", creators, collection_view
    )
