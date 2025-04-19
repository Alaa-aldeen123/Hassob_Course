import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import date
from tabulate import tabulate


# get data form web
def get_book_data(page):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'}
    response = requests.get(url, headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find('ol', class_="row")

        # get image link
        imgs_tags = books.find_all('img', class_="thumbnail")
        imgs = [f'https://books.toscrape.com/{img.get('src')}' for img in imgs_tags]

        # get stars_rating
        re_stars = r'<p\sclass="star-rating\s(\w+)">'
        stars_rating = re.findall(re_stars, str(books))

        # get books_names
        books_names_tags = books.find_all('h3')
        books_names = [book_name.a.get('title') for book_name in books_names_tags]

        # get books prices
        prices_tags = books.find_all('p', class_="price_color")
        prices = [float(price.text[1:]) for price in prices_tags]

        # zip all data
        data = zip(books_names, prices, stars_rating, imgs)
        return data
    return []


# save data in text file
def get_book_text():
    today = date.today().strftime('%d/%m/%Y')
    all_data = []

    for page in range(1, 51):
        page_data = get_book_data(page)
        if not page_data:
            break
        all_data.extend(page_data)
    with open('output.text', 'w',encoding='utf-8') as f:
        f.write('Books library' + '\n')
        f.write(f'date: {today}' + '\n')
        f.write('=' * 30 + '\n')
        table = tabulate(all_data, headers=['Book Name', 'Price (£)', 'Stars Rating', 'Image'], tablefmt='grid')
        f.write(table)


#save data in json file
def get_book_json():
    today = date.today().strftime('%d/%m/%Y')
    all_data=[]

    for page in range(1,51):
        page_data=get_book_data(page)
        if not page_data:
            break
        all_data.extend(page_data)
    title = 'Book Library'
    books = [{'Book Name': books_names, 'Price': prices, 'Stars Rating': stars_rating, 'Image': imgs} for
             books_names, prices, stars_rating, imgs in all_data]
    books_json = {'Title': title, 'Date: ': today, 'Books': books}
    with open('output.json', 'w') as f:
        json.dump(books_json,f)


if __name__ == '__main__':
    get_book_text()
    get_book_json()



