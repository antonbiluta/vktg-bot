import requests
from bs4 import BeautifulSoup


def parse_div(div):
    title = div.find('h2', )


def WhatDay():
    url = 'https://sptoday.ru/kakoj-segodnya-prazdnik/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    divs = soup.find_all('div', {'class': 'prazdnik'})
    for item in divs:
        print(item.find('ul'))

def horoscope():
    url = 'https://sptoday.ru/kakoj-segodnya-prazdnik/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    divs = soup.find_all('div', {'class': 'prazdnik'})
    for item in divs:
        print(item.find('ul'))

WhatDay()