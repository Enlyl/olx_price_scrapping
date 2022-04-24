import csv
import requests
from bs4 import BeautifulSoup

PATH = 'readers.csv'
readers = []

u = 'https://www.olx.ua/elektronika/planshety-el-knigi-i-aksessuary/elektronnye-knigi/?page=1'
# u = input('Введите страничку: ')

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36',
    'accept': '*/*'
}


def save_file(path, items):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Назвнаие модели', 'Цена', 'Место продажи'
        ])
        for reader in items:
            writer.writerow([
                reader['name'],
                reader['price'],
                reader['location']
            ])


def get_html(html):
    r = requests.get(html, headers=HEADERS)
    return r


def get_max_page(html):
    r = get_html(html)
    soup = BeautifulSoup(r.content, 'html.parser')
    max_page = soup.findAll('a', {'class': 'lheight24'})[-1].text

    return int(max_page)


def get_cars(html):
    r = get_html(html)
    soup = BeautifulSoup(r.content, 'html.parser')
    cards = soup.findAll('div', {'class': 'offer-wrapper'})
    print(f'Всего читалок: {len(readers)}')

    for card in cards:
        data = {}

        name = card.find('strong').text
        try:
            price = card.find('p', {'class': 'price'}).text
        except Exception as error:
            price = "Цену уточняйте"
        location = card.find('td', {'class': 'bottom-cell'}).find('div', {'class': 'space'}).find('span').text

        data['name'] = name
        data['price'] = price
        data['location'] = location

        print(data)

        readers.append(data)


def main():
    base_url = u[:-1]
    mp = get_max_page(u)
    for i in range(1, mp + 1):
        current_url = base_url + str(i)
        print(f'Идёт обработка страницы: {current_url}')
        get_cars(current_url)


main()

save_file(PATH, readers)

print(f'Всего читалок: {len(readers)}')

