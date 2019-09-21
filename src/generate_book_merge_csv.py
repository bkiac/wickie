import csv

from prepare import prepare_books_for_merge
from settings import books_merge_csv
from generate_merge_csv import generate_merge_csv


def main():
    books = prepare_books_for_merge()
    generate_merge_csv(books_merge_csv, books)


main()
