import csv
import os

COLUMNS = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
           'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
           'image_url']


def write_csv_files_titles():
    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(COLUMNS)
        print("Colonnes écrites")


def write_line(line: list):
    with open('result.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(line)


def delete_csv_file():
    # Try to delete the csv file it does exist. If not, print a message.
    try:
        os.remove('result.csv')
    except FileNotFoundError:
        print("File result.csv not found. Nothing deleted, will be created again.")
