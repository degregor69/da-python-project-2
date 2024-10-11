from unicodedata import category

import requests
import time
from bs4 import BeautifulSoup

from functions import load

RATING_CORRESPONDING_DICT = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

BASE_URL = 'https://books.toscrape.com/catalogue/'


def extract_book_information(url: str) -> list:
    get_url = requests.get(url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, 'html.parser')

    # product_page_url
    product_page_url = url

    # title
    title = soup.find('h1')
    if title:
        title = title.text

    # product information
    table = soup.find('table', class_='table table-striped')
    all_td = table.find_all('td')
    upc = all_td[0].text
    price_excluding_tax = all_td[2].text.split('£')[-1]
    price_including_tax = all_td[3].text.split('£')[-1]
    number_available = all_td[-2].text
    number_available = number_available[number_available.find("(") + 1:number_available.find(")")]

    # product description
    product_description = "Description not found"
    product_description_div = soup.find('div', id='product_description')
    if product_description_div:
        product_description_p = product_description_div.find_next_sibling('p')
        product_description = product_description_p.text

    # category
    category_link = soup.find_all('a')[3]
    category = category_link.text

    # review rating
    product_main = soup.find("div", class_="col-sm-6 product_main")
    product_main_p = product_main.find_all("p")
    rating_as_text = product_main_p[2]["class"][-1]
    rating = RATING_CORRESPONDING_DICT[rating_as_text]

    # image url
    image = soup.find("img")
    image_url = image["src"]

    return [product_page_url, upc, title, price_excluding_tax, price_including_tax, number_available,
            product_description,
            category, rating, image_url]


def extract_book_information_as_dict(url: str) -> dict:
    get_url = requests.get(url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, 'html.parser')

    # product_page_url
    product_page_url = url

    # title
    title = soup.find('h1')
    if title:
        title = title.text

    # product information
    table = soup.find('table', class_='table table-striped')
    all_td = table.find_all('td')
    upc = all_td[0].text
    price_excluding_tax = all_td[2].text.split('£')[-1]
    price_including_tax = all_td[3].text.split('£')[-1]
    number_available = all_td[-2].text
    number_available = number_available[number_available.find("(") + 1:number_available.find(")")]

    # product description
    product_description = "Description not found"
    product_description_div = soup.find('div', id='product_description')
    if product_description_div:
        product_description_p = product_description_div.find_next_sibling('p')
        product_description = product_description_p.text

    # category
    category_link = soup.find_all('a')[3]
    category = category_link.text

    # review rating
    product_main = soup.find("div", class_="col-sm-6 product_main")
    product_main_p = product_main.find_all("p")
    rating_as_text = product_main_p[2]["class"][-1]
    rating = RATING_CORRESPONDING_DICT[rating_as_text]

    # image url
    image = soup.find("img")
    image_url = image["src"]

    return {
        "product_page_url": product_page_url,
        "title": title,
        "upc": upc,
        "price_excluding_tax": price_excluding_tax,
        "price_including_tax": price_including_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "rating": rating,
        "image_url": image_url
    }


def find_next(url: str):
    get_url = requests.get(url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, 'html.parser')
    pager = soup.find("ul", class_="pager")
    if pager:
        next = pager.find("li", class_="next")
        if next:
            return next.find('a')["href"]
    return


def extract_all_categories_links(url: str):
    base_url = "https://books.toscrape.com/"
    get_url = requests.get(url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, 'html.parser')
    nav_list = soup.find("ul", class_="nav nav-list")
    categories_links = nav_list.find_all("li")[1:]
    categories_list = []
    for category_link in categories_links:
        cat_a = category_link.find("a")
        cat_name = cat_a.text.strip()
        cat_url = f"{base_url}{cat_a['href']}"
        categories_list.append({"cat_url": cat_url, "cat_name": cat_name})
    return categories_list


def extract_categories_pages(url: str):
    categories_pages = [url]
    base_url = url.split("index.html")[0]
    next_url = find_next(url)
    while next_url:
        constructed_url = f"{base_url}{next_url}"
        categories_pages.append(constructed_url)
        next_url = find_next(constructed_url)
    return categories_pages


def extract_books_links_from_category(url: str):
    books_links = []
    get_url = requests.get(url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, 'html.parser')
    ol = soup.find('ol', class_='row')
    books_h3 = ol.find_all('h3')
    for h3 in books_h3:
        a_tag = h3.find('a')
        if not a_tag:
            continue
        books_links.append(extract_book_link(a_tag))
    return books_links


def extract_book_link(a_tag):
    if a_tag and 'href' in a_tag.attrs:
        splitted_link = a_tag['href'].split('../../../')[-1]
        url_to_extract = f"{BASE_URL}{splitted_link}"
        return url_to_extract


def run():
    start_time = time.time()
    load.delete_csv_file()
    load.write_csv_files_titles()

    url = 'https://books.toscrape.com//index.html'
    categories_links_and_names = extract_all_categories_links(url)
    print("Les liens et les noms des catégories ont été extraits.")
    for category in categories_links_and_names:
        print(f"Début de l'extraction de la catégorie : {category.get('cat_name')}")
        cat_url = category['cat_url']
        categories_pages = extract_categories_pages(cat_url)
        for category_page in categories_pages:
            book_links = extract_books_links_from_category(category_page)
            for book_url in book_links:
                line_to_write = extract_book_information(book_url)
                load.write_line(line_to_write)

    # # Calculate the execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f'Extraction done. Execution time: {execution_time:.2f} seconds.')
    # url = "https://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html"
    # extract_book_information_as_dict(url)


if __name__ == "__main__":
    run()
