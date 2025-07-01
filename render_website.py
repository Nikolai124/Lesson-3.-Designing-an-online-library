from jinja2 import Environment, FileSystemLoader, select_autoescape
from math import ceil
from more_itertools import chunked
from livereload import Server
import json
import os


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    os.makedirs('pages', exist_ok=True)
    with open("books/meta_data.json", "r", encoding='utf-8') as books:
        books = books.read()
    books = json.loads(books)
    website_pages = list(chunked(books, 10))
    pages_count = len(website_pages) + 1
    for number, website_page in enumerate(website_pages, 1):
        books = list(chunked(website_page, 2))
        rendered_page = template.render(
            books=books,
            pages_count=pages_count, #кол-во страниц
            current_page_number=number #номер текущей страницы
        )
        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
