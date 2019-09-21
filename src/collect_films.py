import os
import csv
import simplejson as json
from omdb import OMDBClient

from settings import folder, OMDB_API_KEY

films_csv = os.path.join(folder, "films.csv")
films_json = os.path.join(folder, "films.json")

omdb = OMDBClient(apikey=OMDB_API_KEY)

film_titles = []
with open(films_csv, newline="") as f:
    reader = csv.reader(f)
    for film_title in reader:
        film_titles.append(film_title[0])

films = []
for film_title in film_titles:
    print("Searching for '" + film_title + "'")
    res = omdb.request(t=film_title)
    films.append(json.loads(res.content))

with open(films_json, "w") as f:
    json.dump(films, f, indent=2)
