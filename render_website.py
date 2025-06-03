from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


with open("books/meta_data.json", "r", encoding='utf-8') as books:
    books = books.read()
books = json.loads(books)
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
rendered_page = template.render(
    books=books
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
