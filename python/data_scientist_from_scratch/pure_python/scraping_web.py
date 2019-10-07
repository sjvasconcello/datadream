# Scraping Web

import json
from typing import Dict, Set
from bs4 import BeautifulSoup
import requests
import re

url = ("https://raw.githubusercontent.com/"
       "joelgrus/data/master/getting-data.html")
html = requests.get(url).text
soup = BeautifulSoup(html, 'html5lib')

first_paragraph = soup.find('p')

first_paragraph_text = soup.p.text
first_paragraph_words = soup.p.text.split()

first_paragraph_id = soup.p['id']  # Devuelve KeyError si no hay 'id'
first_paragraph_id2 = soup.p.get('id')  # Retorna None si no hay 'id'

all_paragraphs = soup.find_all('p')
paragraphs_with_ids = [p for p in soup('p') if p.get('id')]

important_paragraph = soup('p', {'class': 'important'})
important_paragraph2 = soup('p', 'importat')
important_paragraph3 = [p for p in soup(
    'p') if 'important' in p.get('class', [])]

spans_inside_divs = [span
                     for div in soup('div')
                     for span in soup('span')]

# Example

url = "https://www.house.gov/representatives"
text = requests.get(url).text
soup = BeautifulSoup(text, "html5lib")

all_urls = [a['href']
            for a in soup('a')
            if a.has_attr('href')]

print(len(all_urls))

regex = r"^https?://.*\.house\.gov/?$"

assert re.match(regex, "http://joel.house.gov")
assert re.match(regex, "https://joel.house.gov")
assert re.match(regex, "http://joel.house.gov/")
assert re.match(regex, "https://joel.house.gov/")
assert not re.match(regex, "joel.house.gov")
assert not re.match(regex, "http://joel.house.com")
assert not re.match(regex, "http://joel.house.gov/bigraphy")

good_urls = [url for url in all_urls if re.match(regex, url)]

print(len(good_urls))

html = requests.get("https://jayapal.house.gov").text
soup = BeautifulSoup(html, 'html5lib')

links = {a['href'] for a in soup('a') if 'press releases' in a.text.lower()}
print(links)


####
# JSON and XML
####


