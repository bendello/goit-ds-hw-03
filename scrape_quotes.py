import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "http://quotes.toscrape.com"

def get_quotes_from_page(soup):
    quotes = []
    for quote in soup.select(".quote"):
        text = quote.select_one(".text").get_text(strip=True)
        author = quote.select_one(".author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select(".tag")]
        quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })
    return quotes

def get_author_details(author_url):
    response = requests.get(BASE_URL + author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.select_one(".author-title").get_text(strip=True)
    birth_date = soup.select_one(".author-born-date").get_text(strip=True)
    birth_location = soup.select_one(".author-born-location").get_text(strip=True)
    description = soup.select_one(".author-description").get_text(strip=True)
    return {
        "name": name,
        "birth_date": birth_date,
        "birth_location": birth_location,
        "description": description
    }

def scrape_quotes_and_authors():
    quotes = []
    authors = {}
    page = 1

    while True:
        print(f"Scraping page {page}...")
        response = requests.get(f"{BASE_URL}/page/{page}")
        if "No quotes found!" in response.text:
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_on_page = get_quotes_from_page(soup)
        quotes.extend(quotes_on_page)

        for quote in soup.select(".quote"):
            author_url = quote.select_one("span > a")["href"]
            author_name = quote.select_one(".author").get_text(strip=True)
            if author_name not in authors:
                authors[author_name] = get_author_details(author_url)
                time.sleep(1)  # Додаємо затримку для уникнення блокування

        page += 1

    return quotes, authors

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    quotes, authors = scrape_quotes_and_authors()
    save_to_json(quotes, "quotes.json")
    save_to_json(authors, "authors.json")
    print("Scraping completed and data saved to quotes.json and authors.json")
