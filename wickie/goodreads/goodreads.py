import simplejson as json
import requests
import xmltodict
from bs4 import BeautifulSoup
import re
from dateutil.parser import parse as parse_date
import urllib.parse

from wickie.settings import GOODREADS_API_KEY, GOODREADS_API_SECRET


def create_book_url(title):
    return "https://www.goodreads.com/book/title?id={}".format(
        urllib.parse.quote(title)
    )


def search_book_by_title(title):
    url = "https://www.goodreads.com/search/index.xml?key={}&q={}".format(
        GOODREADS_API_KEY, urllib.parse.quote(title)
    )
    r = requests.get(url)
    content = xmltodict.parse(r.content)
    matches = content["GoodreadsResponse"]["search"]["results"]["work"]
    # Return the the title of the best match if there are more than one
    if isinstance(matches, list):
        return matches[0]["best_book"]["title"]
    return matches["best_book"]["title"]


def scrape_title(soup):
    meta_title = soup.find("meta", attrs={"property": "og:title"})["content"]
    return re.sub(r" by [a-zA-Z ]*", "", meta_title.strip())


def extract_author_names(author_name_containers):
    authors_without_extra_roles = [
        author.a.span.string
        for author in author_name_containers
        if author.find(class_="role") is None
    ]
    return authors_without_extra_roles


def scrape_authors(soup):
    authors = soup.find(id="bookAuthors")
    author_name_containers = extract_author_names(
        authors.find_all(class_="authorName__container")
    )
    return author_name_containers


def extract_publication_date(publication_details):
    """
        Example `parts` array:
        ['Published', 'June 3rd 2003', 'by Modern Library', '(first published 1927)']
        the last item doesn't necessarily exist
    """
    parts = [
        d.strip()
        for d in publication_details.get_text().split("\n")
        if d.strip() != ""
    ]

    # e.g.: June 3rd 2003
    r_spd = r"([A-Z][a-z]*) ([0-9]*[a-z]*) ([0-9]*)"
    specific_publication_date = next(
        (p for p in parts if re.fullmatch(r_spd, p) is not None), None
    )

    # e.g.: (first published 1927)
    r_fpd = r"(\(first published )(.*)(\))"
    first_publication_date = next(
        (
            p.strip("(first published")[:-1]
            for p in parts
            if re.fullmatch(r_fpd, p) is not None
        ),
        None,
    )

    return (
        first_publication_date
        if first_publication_date is not None
        else specific_publication_date
    )


def scrape_publication_date(soup):
    details = soup.find(id="details").find_all(class_="row")
    if len(details) > 0:
        # Find the publication details row after page number row
        publication_details = details[1]
        publication_date = extract_publication_date(publication_details)
        return publication_date
    return ""


def scrape_genres(soup):
    # e.g.: ['Classics', '394 users']
    genres = [
        g.string
        for g in soup.find_all(class_="bookPageGenreLink")
        # Remove how many users marked the genre
        if re.fullmatch(r"[,0-9]* users?", g.string) is None
    ]
    return list(set(genres))


def scrape_cover_image(soup):
    return soup.find(id="coverImage")["src"]


def scrape_book(soup):
    return {
        "title": scrape_title(soup),
        "authors": scrape_authors(soup),
        "publication_date": scrape_publication_date(soup),
        "genres": scrape_genres(soup),
        "cover_image": scrape_cover_image(soup),
    }


def get_book(full_title):
    url = create_book_url(full_title)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return {"url": url, **scrape_book(soup)}
