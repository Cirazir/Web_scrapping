import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

BASE_URL = 'https://habr.com'
FRESH_URL = BASE_URL + '/ru/articles/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


def main():
    response = requests.get(FRESH_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article', class_='tm-articles-list__item')
    print(f'Найдено статей: {len(articles)}')


if __name__ == '__main__':
    main()

def parse_article(article):
    """Достаём из карточки дату, заголовок и ссылку."""
    title_link = article.find('h2', class_='tm-title').find('a', class_='tm-title__link')
    title = title_link.get_text(strip=True)

    href = title_link['href']  # может быть относительной (/ru/articles/123/)
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
        if article.find('h2', class_='tm-title') is None:   # пропускаем промо-блоки без заголовка
            continue

        date, title, link = parse_article(article)
        # вся доступная preview-информация карточки одним текстом
        preview_text = article.get_text(' ', strip=True)

        if find_keywords(preview_text):
            print(f'{date} – {title} – {link}')