import csv

from prepare import prepare_films_for_merge
from settings import films_merge_csv
from generate_merge_csv import generate_merge_csv


def main():
    films = prepare_films_for_merge()
    generate_merge_csv(films_merge_csv, films)


main()
