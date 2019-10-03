import re

from omdb import OMDBClient

from wickie.settings import OMDB_API_KEY

r_imdb_url = r"https?://(w{3}.)?imdb.com/title/(tt[0-9]*)/?"
client = OMDBClient(apikey=OMDB_API_KEY)


def extract_id(url):
    match = re.match(r_imdb_url, url)
    if match:
        return match.groups()[-1]
    return None
