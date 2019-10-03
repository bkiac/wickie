from datetime import datetime


def format_date(datetime_):
    return datetime_.strftime("%Y/%m/%d")


def join(list_, by=","):
    return by.join(list_)


def prettier(dict_):
    string = ""
    for key, value in dict_.items():
        prettier_value = value
        if isinstance(value, int):
            prettier_value = str(value)
        if isinstance(value, list):
            prettier_value = join(value)
        if isinstance(value, datetime):
            prettier_value = format_date(value)
        string = "{}{}: {}\n".format(string, key, prettier_value)
    return string
