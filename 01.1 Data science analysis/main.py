from bs4 import BeautifulSoup
import json
import numpy as np
import requests
from requests.exceptions import MissingSchema  # Add this import statement
import spacy
import trafilatura
import csv

urls = ['https://website.understandingdata.com/', 'https://sempioneer.com/']
data = {}

for url in urls:
    # 1. Obtain the response:
    resp = requests.get(url)
    
    # 2. If the response content is 200 - Status Ok, Save The HTML Content:
    if resp.status_code == 200:
        data[url] = resp.text

def beautifulsoup_extract_text_fallback(response_content):
    '''
    This is a fallback function, so that we can always return a value for text content.
    Even for when both Trafilatura and BeautifulSoup are unable to extract the text from a 
    single URL.
    '''
    # Create the BeautifulSoup object:
    soup = BeautifulSoup(response_content, 'html.parser')
    
    # Finding the text:
    text = soup.find_all(text=True)
    
    # Remove unwanted tag elements:
    cleaned_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
    ]

    # Then we will loop over every item in the extracted text and make sure that the BeautifulSoup4 tag
    # is NOT in the blacklist
    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)
            
    # Remove any tab separation and strip the text:
    cleaned_text = cleaned_text.replace('\t', '')
    return cleaned_text.strip()

def extract_text_from_single_web_page(url):
    downloaded_url = trafilatura.fetch_url(url)
    try:
        a = trafilatura.extract(downloaded_url, output_format="json", with_metadata=True, include_comments=False,
                            date_extraction_params={'extensive_search': True, 'original_date': True})
    except AttributeError:
        a = trafilatura.extract(downloaded_url, output_format="json", with_metadata=True,
                            date_extraction_params={'extensive_search': True, 'original_date': True})
    if a:
        json_output = json.loads(a)
        return json_output['text']
    else:
        try:
            resp = requests.get(url)
            # We will only extract the text from successful requests:
            if resp.status_code == 200:
                return beautifulsoup_extract_text_fallback(resp.content)
            else:
                # This line will handle any failures in both the Trafilature and BeautifulSoup4 functions:
                return np.nan
        # Handling for any URLs that don't have the correct protocol
        except MissingSchema:
            return np.nan

# Add a fake URL to test the exception handling
urls = urls + ['fake_url']

text_content = [extract_text_from_single_web_page(url) for url in urls]

cleaned_textual_content = [text for text in text_content if str(text) != 'nan']

nlp = spacy.load("en_core_web_sm")
for cleaned_text in cleaned_textual_content:
    # 1. Create an NLP document with spaCy:
    doc = nlp(cleaned_text)
    # 2. Spacy has tokenized the text content:
    print(f"This is a spaCy token: {doc[0]}")
    # 3. Extracting the word count per text document:
    print(f"The estimated word count for this document is: {len(doc)}.")
    # 4. Extracting the number of sentences:
    print(f"The estimated number of sentences in the document is: {len(list(doc.sents))}")
    print('\n')

# Adding data to a list for CSV
csv_data = []
for url, text in zip(urls, text_content):
    csv_data.append([url, text])

# CSV file path
csv_file = "collected_data.csv"

# Save data to the CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["URL", "Text"]
    writer = csv.writer(csvfile)
    
    writer.writerow(fieldnames)  # Write header row
    writer.writerows(csv_data)  # Write data rows