import requests

import json

import unicodedata

from fake_headers import Headers

from bs4 import BeautifulSoup


def get_headers():

    return Headers(browser='firefox', os='win').generate()


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

main_page = requests.get(HOST, headers=get_headers()).text
bs = BeautifulSoup(main_page, features='lxml')

articles_list = bs.find(id='a11y-main-content')
articles_tags = articles_list.find_all(class_='vacancy-serp-item-body__main-info')

data_list = list()

for tag in articles_tags:

    link = tag.find('a')['href']

    title = tag.find('h3').find('span').text

    article_link = requests.get(link, headers=get_headers()).text
    article_link_bs = BeautifulSoup(article_link, features='lxml')

    article_salary = article_link_bs.find('div', {'data-qa': 'vacancy-salary'}).text
    salary = unicodedata.normalize('NFKD', article_salary)

    location = tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}, class_='bloko-text').text

    description = article_link_bs.find(class_='vacancy-section').text
    if ("Django" or "Flask" or "django" or "flask") in description:
        data_list.append({
            'link': link,
            'salary': salary,
            'title': title,
            'location': location
        })

with open('data_file.json', 'w', encoding='utf-8') as data:
    json.dump(data_list, data, indent=2, ensure_ascii=False)
