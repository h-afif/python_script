import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import time

def download_pdf(url, save_path):
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded {save_path}")
            return
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {save_path}: {e}")
            if attempt + 1 == retries:
                print(f"Failed to download {save_path} after {retries} attempts.")
            else:
                time.sleep(2)  # Wait a bit before retrying

def convert_to_filename(book_title):
    return book_title.replace(" ", "_")

def search_google_and_download_pdf(book_title, save_directory):
    book_filename = convert_to_filename(book_title)
    base_url = "https://www.google.com/search"
    params = {
        "q": f"{book_title} filetype:pdf ext:pdf",
        "num": 10
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if ".pdf" in href:
            if href.startswith("/url?q="):
                href = href.split("/url?q=")[1].split("&")[0]
            if not href.startswith("http"):
                href = "https://" + href
            pdf_links.append(href)

    if not pdf_links:
        print(f"No PDFs found for '{book_title}' in Google search.")
        return

    pdf_url = pdf_links[0]
    pdf_extension = ".pdf"
    pdf_filename = f"{book_filename}{pdf_extension}"
    pdf_path = os.path.join(save_directory, pdf_filename)
    download_pdf(pdf_url, pdf_path)

def process_books_from_file(file_path, save_directory):
    try:
        with open(file_path, 'r') as file:
            book_titles = file.readlines()
        for book_title in book_titles:
            book_title = book_title.strip()
            if book_title:
                search_google_and_download_pdf(book_title, save_directory)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
script_directory = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(script_directory, "book_titles.txt")  # Ensure the path is correct

# Directory to save PDFs
pdf_directory = os.path.join(script_directory, "pdfs_books")
os.makedirs(pdf_directory, exist_ok=True)

process_books_from_file(text_file_path, pdf_directory)
