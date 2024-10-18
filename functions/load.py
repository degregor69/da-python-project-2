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


import os
import shutil


def create_pictures_file():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    pictures_dir = os.path.join(parent_directory, 'pictures')

    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)
        print(f"Le dossier 'pictures' a été créé à ce chemin :  {pictures_dir}")
        return

    for filename in os.listdir(pictures_dir):
        file_path = os.path.join(pictures_dir, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    print("Le fichier pictures existe déjà. Tous les éléments à l'intérieur ont été supprimés.")


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
