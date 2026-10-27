import time

import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

BASE_URL = 'https://habr.com'
FRESH_URL = BASE_URL + '/ru/articles/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


def parse_article(article):
    title_link = article.find('h2', class_='tm-title').find('a', class_='tm-title__link')
    title = title_link.get_text(strip=True)
    href = title_link['href']
    link = href if href.startswith('http') else BASE_URL + href
    time_tag = article.find('time')
    date = time_tag.get('title') or time_tag.get('datetime', '')
    return date, title, link


def find_keywords(text):
    text = text.lower()
    return [kw for kw in KEYWORDS if kw.lower() in text]


def main():
    response = requests.get(FRESH_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    for article in soup.find_all('article', class_='tm-articles-list__item'):
        if article.find('h2', class_='tm-title') is None:
            continue

        date, title, link = parse_article(article)

        if find_keywords(article.get_text(' ', strip=True)):
            print(f'{date} – {title} – {link}')
            continue

        article_response = requests.get(link, headers=HEADERS)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        body = article_soup.find('div', class_='article-formatted-body')
        if body and find_keywords(body.get_text(' ', strip=True)):
            print(f'{date} – {title} – {link}')

        time.sleep(0.5)


if __name__ == '__main__':
    main()