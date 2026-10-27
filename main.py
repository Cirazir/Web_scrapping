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