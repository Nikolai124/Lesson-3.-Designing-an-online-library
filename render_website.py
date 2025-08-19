import json
import os


from dotenv import load_dotenv
from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    os.makedirs('pages', exist_ok=True)
    meta_data = os.getenv('META_DATA', default="meta_data.json")
    with open(meta_data, "r", encoding='utf-8') as file:
        books = json.load(file)
    website_pages = list(chunked(books, 10))
    pages_count = len(website_pages) + 1
    for number, website_page in enumerate(website_pages, 1):
        rendered_page = template.render(
            books=website_page,
            pages_count=pages_count,
            current_page_number=number
        )
        with open(f'pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.', default_filename='../pages/index1.html')
