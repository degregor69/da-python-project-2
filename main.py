import requests
from bs4 import BeautifulSoup

rating_corresponding_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def extract_book_information(url: str):
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
   number_available = all_td[-1].text
   number_available = number_available[number_available.find("(")+1:number_available.find(")")]

   # product description
   product_information_paragraph = soup.find_all("p", )[-1]
   product_information = product_information_paragraph.text

   # category
   category_link = soup.find_all('a')[-1]
   category = category_link.text

   # review rating
   product_main = soup.find("div", class_="col-sm-6 product_main")
   product_main_p = product_main.find_all("p")
   rating_as_text = product_main_p[2]["class"][-1]
   rating = rating_corresponding_dict[rating_as_text]

   # image url
   image = soup.find("img")
   image_url = image["src"]

   print(product_page_url, title, upc, price_excluding_tax, price_including_tax, number_available, product_information, category, rating, image_url)




if __name__ == "__main__":
   url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
   extract_book_information(url)