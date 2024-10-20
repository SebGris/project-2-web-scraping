import os
import csv
from urllib import parse as urlparse

import requests
from bs4 import BeautifulSoup


### Constants
HOME_URL = "http://books.toscrape.com/"


### Functions
def get_category_url_by_page_number(category_page, page_number):
    return urlparse.urljoin(category_page, f"page-{page_number}.html")


def extract_book_links(soup: BeautifulSoup):
    return [
        convert_href_to_book_url(h3.find("a").get("href"))
        for h3 in soup.find("ol").find_all("h3")
    ]


def extract_book(category_page):
    category_response = requests.get(category_page)
    if category_response.ok:
        soup = BeautifulSoup(category_response.content, "lxml")
        return extract_book_links(soup)
    else:
        print(f"Erreur : cette catégorie n'existe pas ({category_response})")


def convert_href_to_book_url(href):
    return urlparse.urljoin(
        HOME_URL, "/".join(["catalogue", href.rsplit("/")[-2], "index.html"])
    )


def extract_book_informations(product_page_url, soup: BeautifulSoup):
    # Gives the first article tag, the one with the comment <!-- Start of product page -->
    article_tag = soup.find("article")
    information_rows = soup.find_all("tr")
    # Check if the product description exists
    product_description = article_tag.find("div", {"id": "product_description"})
    text_description = (
        "" if product_description is None else product_description.find_next("p").text
    )
    return {
        "product_page_url": product_page_url,
        "universal_product_code": information_rows[0].find("td").text,
        "title": article_tag.h1.text,
        "price_including_tax": information_rows[3].find("td").text,
        "price_excluding_tax": information_rows[2].find("td").text,
        "number_available": information_rows[5].find("td").text,
        "product_description": text_description,
        "category": soup.find("ul", {"class": "breadcrumb"})
        .find_all("li")[-2]
        .find("a")
        .text,
        "review_rating": article_tag.find("p", {"class": "instock availability"})
        .find_next("p")
        .attrs["class"][1],
        "image_url": article_tag.img.attrs["src"],
    }


def get_book_informations_from(book_page_url):
    book_response = requests.get(book_page_url)
    if book_response.ok:
        soup = BeautifulSoup(book_response.content, "lxml")
        return extract_book_informations(book_response.url, soup)
    else:
        print(f"Erreur : ce livre n'existe pas ({book_response})")


def save_image_from_url(image_url, new_filename):
    with open(new_filename, "wb") as handle:
        response = requests.get(image_url)
        handle.write(response.content)


### Main
category_page_test = urlparse.urljoin(HOME_URL, "/catalogue/category/books/default_15/")
category_page_1 = get_category_url_by_page_number(category_page_test, 1)
category_response = requests.get(category_page_1)
if category_response.ok:
    soup = BeautifulSoup(category_response.content, "lxml")
    range_page = soup.find("li", {"class": "current"})
    maximum_page = range_page.text.split("of")[-1].strip()
else:
    print(f"Erreur : cette catégorie n'existe pas ({category_response})")
print(f"Number of pages in the category : {maximum_page}")
url_books_for_one_category = []
for number in range(1, int(maximum_page), 1):
    url_books_for_one_category += extract_book(
        get_category_url_by_page_number(category_page_test, number)
    )
books_informations = []
for url in url_books_for_one_category:
    print(f"Reading the page {url}")
    books_informations.append(get_book_informations_from(url))


### Export to csv file
desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
project_path = os.path.join(desktop_path, "project_web_scraping")
images_path = os.path.join(project_path, "images")
if not os.path.exists(project_path):
    os.makedirs(project_path)
if not os.path.exists(images_path):
    os.makedirs(images_path)
filename = os.path.join(project_path, "books_informations.csv")
with open(filename, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, books_informations[0].keys(), delimiter=";")
    writer.writeheader()
    for book_informations in books_informations:
        print(f"writing in the csv file of this book : {book_informations["title"]}")
        writer.writerow(book_informations)
        save_image_from_url(
            urlparse.urljoin(HOME_URL, book_informations["image_url"]),
            os.path.join(images_path, book_informations["image_url"].rsplit("/")[-1]),
        )
print(f"Data successfully written to {filename}")
