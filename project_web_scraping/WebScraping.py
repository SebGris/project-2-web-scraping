import csv
from datetime import datetime
from pathlib import Path
from urllib import parse as urlparse

import requests
import regex
from bs4 import BeautifulSoup


### Constants
HOME_URL = "http://books.toscrape.com/"


### Functions
def extract_books_from_categories(categories):
    for category_name, category_url in categories:
        url_of_the_books = extract_urls_books_in_category(category_url)
        books_informations = []
        for book_url in url_of_the_books:
            books_informations.append(get_book_informations(book_url))
        category_path = Path.joinpath(project_path, category_name)
        category_path.mkdir(parents=True, exist_ok=True)
        images_path = Path.joinpath(category_path, "images")
        images_path.mkdir(parents=True, exist_ok=True)
        current_date = datetime.now().strftime("%Y-%m-%d")
        export_to_csv_file(
            books_informations,
            Path.joinpath(
                category_path,
                f"{current_date}_category_{category_name}_book_information.csv",
            ),
            images_path,
        )
        books_informations.clear()


def export_to_csv_file(books_informations, filename, images_path):
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file, books_informations[0].keys(), delimiter=";", quotechar='"'
        )
        writer.writeheader()
        for book_informations in books_informations:
            print(
                f'Ecriture dans le csv des informations du livre : {book_informations["title"]}'
            )
            writer.writerow(book_informations)
            old_name_image = Path(book_informations["image_url"]).stem
            save_image_from_url(
                urlparse.urljoin(HOME_URL, book_informations["image_url"]),
                Path.joinpath(
                    images_path,
                    f'{regex.sub(r"[^a-zA-Z0-9 ]", "", book_informations["title"][:100])}_{old_name_image}.jpg',
                ),
            )
    print(f"Les données ont été écrites avec succès dans : {filename}")


def save_image_from_url(image_url, new_filename):
    with open(new_filename, "wb") as handle:
        response = requests.get(image_url)
        handle.write(response.content)


def extract_urls_books_in_category(index_page_of_the_category):
    category_response = requests.get(index_page_of_the_category)
    if category_response.ok:
        url_books = extract_books_urls(index_page_of_the_category)
        soup = BeautifulSoup(category_response.content, "html.parser")
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
        soup = BeautifulSoup(category_response.content, "html.parser")
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
        soup = BeautifulSoup(book_response.content, "html.parser")
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
            "number_available": regex.search(r"\d+", information_rows[5].td.text)[0],
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


### Main
project_path = Path.joinpath(Path.home(), "Desktop", "Books to Scrape")

response = requests.get(HOME_URL)
if not (response.ok):
    print(f"Erreur : pas de réponse du site {HOME_URL} ({response})")
    exit()

soup = BeautifulSoup(response.content, "html.parser")
all_navigable_categories = [
    (a.text.strip(), urlparse.urljoin(HOME_URL, a["href"]))
    for a in soup.find("ul", {"class": "nav nav-list"}).find_all("a", href=True)
]
all_navigable_categories.sort()
categories_by_name = {name: url for name, url in all_navigable_categories}
categories_by_name["Toutes les catégories"] = categories_by_name.pop("Books")


### Build menu
categories_menu = {
    index: name for index, name in enumerate(categories_by_name, start=1)
}
for key, value in categories_menu.items():
    print(f"{key} : {value}")
print("Choix des catégories à exporter.")
number_selected_categories = input(
    "Entrez un n° de catégorie, ou plusieurs n° de catégorie séparés par des virgules (entrez 0 pour quitter) : "
)
number_selected_categories = [int(x) for x in number_selected_categories.split(",")]
if number_selected_categories[0] == 0:
    exit()
if number_selected_categories[0] == len(categories_menu):
    number_selected_categories = list(range(1, len(categories_menu)))
name_selected_categories = [categories_menu[key] for key in number_selected_categories]
selected_categories = [
    (key, value)
    for key, value in categories_by_name.items()
    if key in name_selected_categories
]
extract_books_from_categories(selected_categories)
