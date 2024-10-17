import csv
import os

COLUMNS = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
           'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
           'image_url']


def write_csv_files_titles(filename: str):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(COLUMNS)


def write_line(filepath: str, line: list):
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(line)


def create_category_file(cat_name: str):
    # Build the path to the 'extractions' folder'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    extractions_directory = os.path.join(current_directory, '..', 'extractions')

    if not os.path.exists(extractions_directory):
        os.makedirs(extractions_directory)

    filename = os.path.join(extractions_directory, f"{cat_name}.csv")
    delete_csv_file(filename)
    write_csv_files_titles(filename)

    print(f"Fichier pour la catégorie : {cat_name} créé. ")
    return filename


def delete_csv_file(filename: str):
    # Try to delete the csv file if it exists. If not, print a message.
    try:
        os.remove(filename)
    except FileNotFoundError:
        print(f"File {filename} not found. Nothing deleted, will be created again.")
