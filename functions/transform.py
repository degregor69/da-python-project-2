from bs4 import BeautifulSoup

RATING_CORRESPONDING_DICT = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_book_title(soup: BeautifulSoup):
    title = soup.find('h1')
    if not title:
        return
    return title.text


def get_product_information(soup: BeautifulSoup):
    table = soup.find('table', class_='table table-striped')
    all_td = table.find_all('td')
    upc = all_td[0].text
    price_excluding_tax = all_td[2].text.split('£')[-1]
    price_including_tax = all_td[3].text.split('£')[-1]
    number_available = all_td[-2].text
    number_available = number_available[number_available.find("(") + 1:number_available.find(")")]
    number_available = number_available.split(" ")[0]
    return upc, price_excluding_tax, price_including_tax, number_available


def get_product_description(soup: BeautifulSoup):
    product_description_div = soup.find('div', id='product_description')
    if not product_description_div:
        return "Description not available"
    product_description_p = product_description_div.find_next_sibling('p')
    return product_description_p.text


def get_category(soup: BeautifulSoup):
    category_link = soup.find_all('a')[3]
    if not category_link:
        return "Category not available"
    return category_link.text


def get_rating(soup: BeautifulSoup):
    product_main = soup.find("div", class_="col-sm-6 product_main")
    product_main_p = product_main.find_all("p")
    rating_as_text = product_main_p[2]["class"][-1]
    return RATING_CORRESPONDING_DICT.get(rating_as_text)


def get_image_url(soup: BeautifulSoup):
    image = soup.find("img")
    image_src = image.get("src")
    if not image_src:
        return "Image not available"
    base_url = "https://books.toscrape.com/"
    img_url = image_src.split("../../")[-1]
    return base_url + img_url
