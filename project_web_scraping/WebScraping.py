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
def extract_categories(home_url):
    """Extract all book categories of the site.

    Args:
        home_url (str): The URL of the site to be analysed.

    Returns:
        dict: Returns a dictionary containing the names of the categories and their URLs.
    """
    try:
        response = requests.get(home_url)
        if response.ok:
            soup = BeautifulSoup(response.content, "html.parser")
            book_categories = [
                (a.text.strip(), urlparse.urljoin(home_url, a["href"]))
                for a in soup.find("ul", {"class": "nav nav-list"}).find_all(
                    "a", href=True
                )
            ]
            book_categories.sort()
            return {name: url for name, url in book_categories}
    except requests.exceptions.RequestException:
        return {}


def display_categories_menu():
    for key, value in categories_name.items():
        print(f"{key} : {value}")
    print("Choix des catégories à exporter.")
    print("Entrez 0 pour quitter.")
    print(
        "Entrez un n° de catégorie, ou plusieurs n° de catégorie séparés par des virgules : "
    )


def convert_numbers_selected_to_categories():
    return [
        (key, value)
        for key, value in name_and_url_categories.items()
        if key in [categories_name[key] for key in numbers_selected]
    ]


def extract_books_from_categories(categories):
    for category_name, category_url in categories:
        print(f"Lecture des pages de la catégorie : {category_name}")
        url_of_books = extract_urls_books_in_category(category_url)
        books = [extract_book_informations(url) for url in url_of_books]
        export_to_csv_file(category_name, books)


def extract_urls_books_in_category(index_page_of_the_category):
    response = requests.get(index_page_of_the_category)
    if response.ok:
        url_books = extract_books_urls(index_page_of_the_category)
        soup = BeautifulSoup(response.content, "html.parser")
        range_page = soup.find("li", {"class": "current"})
        maximum_page = int(
            1 if range_page is None else range_page.text.split("of")[-1].strip()
        )
        for page_number in range(2, maximum_page + 1):
            url_books += extract_books_urls(
                urlparse.urljoin(index_page_of_the_category, f"page-{page_number}.html")
            )
        return url_books
    else:
        print(f"Erreur : cette catégorie n'existe pas ({response})")


def extract_books_urls(category_page_url):
    response = requests.get(category_page_url)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        return [
            urlparse.urljoin(category_page_url, h3.a.get("href"))
            for h3 in soup.find_all("h3")  # every link to the book is in an h3
        ]
    else:
        print(f"Erreur : cette page de la catégorie n'existe pas ({response})")


def convert_number_letters_into_number(number_letters):
    numbers = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return numbers[number_letters]


def extract_book_informations(book_page_url):
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
            "image_url": urlparse.urljoin(HOME_URL, article_tag.img.attrs["src"]),
        }
    else:
        print(f"Erreur : ce livre n'existe pas ({book_response})")


def export_to_csv_file(category_name, books):
    project_folder_on_desktop = Path.joinpath(Path.home(), "Desktop", "Books to Scrape")
    category_path = Path.joinpath(project_folder_on_desktop, category_name)
    category_path.mkdir(parents=True, exist_ok=True)
    images_path = Path.joinpath(category_path, "images")
    images_path.mkdir(parents=True, exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = Path.joinpath(
        category_path,
        f"{current_date} Information Livres Catégorie {category_name}.csv",
    )
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, books[0].keys(), delimiter=";", quotechar='"')
        writer.writeheader()
        for book_informations in books:
            print(
                f'Ecriture dans le csv des informations du livre : {book_informations["title"]}'
            )
            writer.writerow(book_informations)
            save_image_from_url(
                book_informations["image_url"],
                Path.joinpath(
                    images_path,
                    f'{regex.sub(r"[^a-zA-Z0-9 ]", "", book_informations["title"][:100])}',
                ),
            )
    print(f"Les données ont été écrites avec succès dans : {filename}")


def save_image_from_url(image_url, filename):
    with open(filename, "wb") as handle:
        response = requests.get(image_url)
        handle.write(response.content)


### Main
name_and_url_categories = extract_categories(HOME_URL)
if not name_and_url_categories:
    print(f"Erreur : pas de réponse du site {HOME_URL}")
name_and_url_categories["Toutes les catégories"] = name_and_url_categories.pop(
    "Books"
)
categories_name = {
    index: name for index, name in enumerate(name_and_url_categories, start=1)
}
display_categories_menu()
numbers_selected = input("")
if numbers_selected in ("0" ,""):
    exit()
numbers_selected = regex.sub(r"[^0-9,]", "", numbers_selected)
numbers_selected = [int(x) for x in numbers_selected.split(",") if x !=""]
if numbers_selected[0] == len(categories_name):
    numbers_selected = list(range(1, len(categories_name)))
selected_categories = convert_numbers_selected_to_categories()
extract_books_from_categories(selected_categories)
print("Fin du traitement : enregistrement des images et fichiers CSV terminé.")
