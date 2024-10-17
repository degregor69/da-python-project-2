import time
from functions import load, extract


def run():
    start_time = time.time()
    url = 'https://books.toscrape.com//index.html'
    categories_links_and_names = extract.extract_all_categories_links(url)
    print("Les liens et les noms des catégories ont été extraits.")
    for category in categories_links_and_names:
        cat_name = category.get("cat_name")
        print(f"Début de l'extraction de la catégorie : {cat_name}")
        filepath = load.create_category_file(cat_name)
        cat_url = category['cat_url']
        categories_pages = extract.extract_categories_pages(cat_url)
        for category_page in categories_pages:
            book_links = extract.extract_books_links_from_category(category_page)
            for book_url in book_links:
                line_to_write = extract.extract_book_information(book_url)
                load.write_line(filepath, line_to_write)

    # # Calculate the execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f'Extraction done. Execution time: {execution_time:.2f} seconds.')


if __name__ == "__main__":
    run()
