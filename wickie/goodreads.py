import re
import requests

from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date


r_goodreads_url = (
    r"https?://(w{3}\.)?goodreads\.com/book/show/([0-9]+).(.*)(\?(.*))?"
)


def _scrape_title(soup):
    meta_title = soup.find("meta", attrs={"property": "og:title"})["content"]
    return re.sub(r" by [a-zA-Z ]*", "", meta_title.strip())


def _extract_author_names(author_name_containers):
    authors_without_extra_roles = [
        author.a.span.string
        for author in author_name_containers
        if author.find(class_="role") is None
    ]
    return authors_without_extra_roles


def _scrape_authors(soup):
    authors = soup.find(id="bookAuthors")
    author_name_containers = _extract_author_names(
        authors.find_all(class_="authorName__container")
    )
    return author_name_containers


def _extract_publication_date(publication_details):
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


def _scrape_publication_date(soup):
    details = soup.find(id="details").find_all(class_="row")
    if len(details) > 0:
        # Find the publication details row after page number row
        publication_details = details[1]
        publication_date = _extract_publication_date(publication_details)
        return publication_date
    return ""


def _scrape_genres(soup):
    # e.g.: ['Classics', '394 users']
    genres = [
        g.string
        for g in soup.find_all(class_="bookPageGenreLink")
        # Remove how many users marked the genre
        if re.fullmatch(r"[,0-9]* users?", g.string) is None
    ]
    return list(set(genres))


def _scrape_cover_image(soup):
    return soup.find(id="coverImage")["src"]


def _scrape_book(soup):
    return {
        "title": _scrape_title(soup),
        "authors": _scrape_authors(soup),
        "publication_date": _scrape_publication_date(soup),
        "genres": _scrape_genres(soup),
        "cover_image": _scrape_cover_image(soup),
    }


def get(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return {"url": url, **_scrape_book(soup)}
