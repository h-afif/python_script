import json
import os

# Function to extract book titles from the JSON file and write to text file
def extract_titles_from_json(json_file_path, output_txt_file_path):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            books = json.load(json_file)
        
        # Extract the titles
        titles = [book["title"] for book in books]
        
        # Write titles to the text file
        with open(output_txt_file_path, 'w') as txt_file:
            for title in titles:
                txt_file.write(title + '\n')
        
        print(f"Extracted {len(titles)} titles to {output_txt_file_path}")
    except FileNotFoundError:
        print(f"File {json_file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {json_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
script_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_directory, "output.json")  # Ensure the path is correct
output_txt_file_path = os.path.join(script_directory, "book_titles.txt")

extract_titles_from_json(json_file_path, output_txt_file_path)
