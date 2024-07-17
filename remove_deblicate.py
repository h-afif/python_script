# Open the links.txt file to read links
with open('links.txt', 'r', encoding='utf-8') as f:
    links = f.readlines()

# Open unique_links.txt to read existing unique links
with open('unique_links.txt', 'r', encoding='utf-8') as f:
    unique_links = set(f.read().splitlines())

# Open unique_links.txt to append new unique links
with open('unique_links.txt', 'a', encoding='utf-8') as f:
    for link in links:
        link = link.strip()  # Remove any leading/trailing whitespace
        if link not in unique_links:
            f.write(link + '\n')
            unique_links.add(link)
