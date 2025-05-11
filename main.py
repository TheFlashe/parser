

import requests
import bs4
from fake_headers import Headers

## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python','одно']


def generate_headers():
    headers = Headers(os='win', browser='chrome').generate()
    return headers


response = requests.get("https://habr.com/ru/articles/", headers=generate_headers())
main_page_html = response.text
main_page_soap = bs4.BeautifulSoup(main_page_html, features="lxml")

tm_articl_list_tag = main_page_soap.find("div", class_="tm-articles-list")
artical_tags = tm_articl_list_tag.find_all("article")

artical_parse = []
for artical_tag in artical_tags:
    h2_tag = artical_tag.find("h2")
    a_tag = h2_tag.find("a")
    time_tag = artical_tag.find("time")
    # print(a_tag)

    artickle_link = a_tag['href']
    artickle_link = f'https://habr.com{artickle_link}'
    articla_time = time_tag["datetime"]
    artical_header = a_tag.text.strip().lower()

    artical_page_response = requests.get(artickle_link, headers=generate_headers())

    artical_page_html = artical_page_response.text
    artical_page_soap = bs4.BeautifulSoup(artical_page_html, features="lxml")
    artical_body_tag = artical_page_soap.find("div", id="post-content-body")

    artical_parsed = {
        'artickle_link': artickle_link,
        'artical_header': artical_header,
        'articla_time': articla_time,
        'artical_body': artical_body_tag
    }
    # preview_text = artical_header.lower()
    # print(artical_parsed)
    for keys, value in artical_parsed.items():
        for key in KEYWORDS:
            if key in value:
                artical_parse.append(f"{articla_time} – {artical_header} – {artickle_link} - найдено слово: {key}")

for article in artical_parse:
    print(article)
