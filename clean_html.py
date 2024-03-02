import os
import glob
from bs4 import BeautifulSoup

def process_html_file(file_path):
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')

    # Remove script, style, and nav elements
    for script_or_style in soup(["script", "style", "nav"]):
        script_or_style.decompose()

    # Get clean text from the parsed HTML
    clean_text = soup.get_text(separator='\n', strip=True)

    # Write the clean text back to the file (or to a new file, if preferred)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(clean_text)

def process_directory(directory_path):
    # Navigate through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        # Find all HTML files in the current directory
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                print(f"Processing {file_path}...")
                process_html_file(file_path)

# Path to the data directory
directory_path = 'webscraper/data'  # Adjust the path as needed
process_directory(directory_path)
