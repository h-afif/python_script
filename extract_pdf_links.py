import json

# Open the output.json file
with open('output.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Extract PDF links from each entry
pdf_links = [entry['pdf'] for entry in data]

# Save the PDF links to pdf_links.txt
with open('pdf_links.txt', 'w', encoding='utf-8') as txt_file:
    for link in pdf_links:
        txt_file.write("https://www.kotobati.com" + link + "\n")

print(f"Extracted {len(pdf_links)} PDF links to pdf_links.txt")
