import os
import csv
from urllib import parse as urlparse

import requests
import regex
from bs4 import BeautifulSoup


### Constants
HOME_URL = "http://books.toscrape.com/"


### Functions
def extract_books_from_categories(categories_url):
    books_url_by_category = [
        extract_urls_books_in_category(category_url) for category_url in categories_url
    ]
    books_informations = []
    for category in books_url_by_category:
        for book_url in category:
            print(f"Lecture de la page : {book_url}")
            books_informations.append(get_book_informations(book_url))
        export_to_csv_file(books_informations, "books_info_.csv")
        books_informations.clear()


def export_to_csv_file(books_informations, filename_csv):
    filename = os.path.join(project_path, filename_csv)
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, books_informations[0].keys(), delimiter=";")
        writer.writeheader()
        for book_informations in books_informations:
            print(
                f'Ecriture dans le csv des informations du livre : {book_informations["title"]}'
            )
            writer.writerow(book_informations)
            save_image_from_url(
                urlparse.urljoin(HOME_URL, book_informations["image_url"]),
                os.path.join(
                    images_path, book_informations["image_url"].rsplit("/")[-1]
                ),
            )
    print(f"Les données ont été écrites avec succès dans : {filename}")


def extract_urls_books_in_category(index_page_of_the_category):
    category_response = requests.get(index_page_of_the_category)
    if category_response.ok:
        url_books = extract_books_urls(index_page_of_the_category)
        soup = BeautifulSoup(category_response.content, "html.parser")  # lxml
        range_page = soup.find("li", {"class": "current"})
        maximum_page = int(
            1 if range_page is None else range_page.text.split("of")[-1].strip()
        )
        print(f"Nombre de pages dans la catégorie : {maximum_page}")
        for page_number in range(2, maximum_page + 1):
            url_books += extract_books_urls(
                urlparse.urljoin(index_page_of_the_category, f"page-{page_number}.html")
            )
        return url_books
    else:
        print(f"Erreur : cette catégorie n'existe pas ({category_response})")


def extract_books_urls(category_page_url):
    category_response = requests.get(category_page_url)
    if category_response.ok:
        soup = BeautifulSoup(category_response.content, "lxml")
        return [
            urlparse.urljoin(category_page_url, h3.a.get("href"))
            for h3 in soup.find_all("h3")  # every link to the book is in an h3
        ]
    else:
        print(f"Erreur : cette page de la catégorie n'existe pas ({category_response})")


def convert_number_letters_into_number(number_letters):
    numbers = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return numbers[number_letters]


def get_book_informations(book_page_url):
    book_response = requests.get(book_page_url)
    if book_response.ok:
        soup = BeautifulSoup(book_response.content, "lxml")
        # Gives the first article tag, the one with the comment <!-- Start of product page -->
        article_tag = soup.find("article")
        # Check if the product description exists
        product_description = article_tag.find("div", {"id": "product_description"})
        text_description = (
            None
            if product_description is None
            else product_description.find_next("p").text
        )
        information_rows = soup.find_all("tr")
        return {
            "product_page_url": book_response.url,
            "universal_product_code": information_rows[0].td.text,
            "title": article_tag.h1.text,
            "price_including_tax": information_rows[3].td.text,
            "price_excluding_tax": information_rows[2].td.text,
            "number_available": regex.search("\d+", information_rows[5].td.text)[0],
            "product_description": text_description,
            "category": soup.find(
                "ul", {"class": "breadcrumb"}
            )  # There are two ul tags
            .find_all("li")[-2]
            .find("a")
            .text,
            "review_rating": convert_number_letters_into_number(
                article_tag.find("p", {"class": "instock availability"})
                .find_next("p")
                .attrs["class"][1]
            ),
            "image_url": article_tag.img.attrs["src"],
        }
    else:
        print(f"Erreur : ce livre n'existe pas ({book_response})")


def save_image_from_url(image_url, new_filename):
    with open(new_filename, "wb") as handle:
        response = requests.get(image_url)
        handle.write(response.content)


def get_path_on_desktop():
    desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    project_path = os.path.join(desktop_path, "project_web_scraping")
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    return project_path


### Main
project_path = get_path_on_desktop()
images_path = os.path.join(project_path, "images")
if not os.path.exists(images_path):
    os.makedirs(images_path)

response = requests.get(HOME_URL)
if response.ok:
    soup = BeautifulSoup(response.content, "lxml")
    categories_url = [
        urlparse.urljoin(HOME_URL, a["href"])
        for a in soup.find("ul", {"class": "nav nav-list"})
        .find("ul")
        .find_all("a", href=True)
    ]
else:
    print(f"Erreur : pas de réponse du site {HOME_URL} ({response})")
menu_categories = {}
for num, url in enumerate(categories_url, start=1):
    category = {}
    category_url_name = url.split("/")[-2]
    category["name"] = category_url_name.split("_")[-2]
    category["url"] = url
    menu_categories[num] = category
for key, value in menu_categories.items():
    print(f"{key} : {value["name"]}")
print("99 : pour toutes les catégories")
print("Choix des catégories à exporter.")
categories_number = input(
    "Entrez un n° de catégorie, ou plusieurs n° de catégorie séparés par des virgules (entrez 0 pour quitter) : "
)
categories_number = [int(x) for x in categories_number.split(",")]
if categories_number[0] == "0":
    exit()
categories_url = [menu_categories[number].get("url") for number in categories_number]
extract_books_from_categories(categories_url)
