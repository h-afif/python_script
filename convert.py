import requests
from bs4 import BeautifulSoup
import os
import json

# Scraping function
def scrape_book_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('div', class_='product__title').find('h1').text.strip()
    description = soup.find('div', class_='product__description').text.strip()
    image_url = soup.find('img', class_='product__image')['src']
    download_link = soup.find('a', class_='product__download-link')['href']

    return {
        'title': title,
        'description': description,
        'image': image_url,
        'pdf': download_link
    }

# Example usage of the scraping function
book_url = 'https://www.kotobati.com/'  # Replace with the actual URL
book_details = scrape_book_details(book_url)

# Save scraped data into a JSON file
output_directory = os.path.join(os.path.dirname(__file__), 'json_files')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

json_filename = os.path.join(output_directory, 'book_details.json')
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(book_details, json_file, indent=4, ensure_ascii=False)

# Combining JSON files into one
combined_data = []

# Check if the directory exists
if os.path.exists(output_directory):
    # Iterate over each file in the directory
    for filename in os.listdir(output_directory):
        if filename.endswith(".json"):
            filepath = os.path.join(output_directory, filename)
            # Read data from each JSON file
            with open(filepath, "r", encoding="utf-8") as infile:
                try:
                    file_data = json.load(infile)
                    if isinstance(file_data, list):
                        combined_data.extend(file_data)
                    else:
                        combined_data.append(file_data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {filepath}")
else:
    print(f"Directory not found: {output_directory}")

# Directory where the script is located
script_directory = os.path.dirname(__file__)

# Write combined data to output.json in the same directory as the script
output_file = os.path.join(script_directory, "output.json")
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(combined_data, outfile, indent=4, ensure_ascii=False)

print(f"Combined data from {len(combined_data)} items saved to {output_file}")
