from flask import Flask, request
from bs4 import BeautifulSoup
import requests

from models import Product

app = Flask(__name__)

###### ***************fetching HTML****************

def search_tunisianet(key):
    html_text = requests.get(
        "https://www.tunisianet.com.tn/recherche?controller=search&orderby=price&orderway=asc&s=" + key + "&submit_search=").text
    return html_text


def search_wiki(key):
    html_text = requests.get(
        "https://www.wiki.tn/recherche?controller=search&orderby=position&orderway=desc&search_query=" + key + "&submit_search=").text
    return html_text


def search_oxtek(key):
    html_text = requests.get(
        "https://www.technopro-online.com/module/iqitsearch/searchiqit?s=" + key).text
    return html_text

###### ********************processing data************************


def get_product_from_tunisianet(soup):
    ## get product name
    products_title = soup.find('h2', class_="h3 product-title")
    if products_title:
        product_name = products_title.text.replace('/', '')

        ## get product link
        product_link = products_title.find('a')['href']

        ## get product reference
        products_ref = soup.find('span', class_="product-reference").text.replace(' ', '')

        ## get product price
        products_price = soup.find('span', class_="price").text.replace(' ', '')

        ## get product image link
        product_img = soup.find('img', class_="center-block img-responsive")['src']

        ## get product availability
        product_availability = soup.find('div', {"id": "stock_availability"}).text.strip()

        product = Product(product_name, products_ref, products_price, product_availability, product_img, product_link)
        return product.toJSON()


def get_product_from_wiki(soup):
    ## get product name
    products_title = soup.find('h4', class_="name")
    if products_title:
        product_name = products_title.text
        product_name, product_reference = product_name.split("-")  ## get product reference

        ## get product price
        products_price = soup.find('span', class_="price product-price").text.replace(' ', '')

        ## get product link
        product_link = products_title.find('a')['href']

        ## get product availability
        product_availability = soup.find('span', class_="availability").text.replace(' ', '').strip()

        ## get product image link
        product_img_div = soup.find('div', class_="product-image-container image")
        product_img = product_img_div.find('img', class_="replace-2x img-responsive")['src']

        product = Product(product_name, product_reference.replace(' ', ''), products_price, product_availability, product_img,
                          product_link)
        return product.toJSON()


def get_product_from_oxtek(soup):
    ## get product name
    products_title = soup.find('h2', class_="h3 product-title")
    if products_title:
        product_name = products_title.text

        ## get product link
        product_link = products_title.find('a')['href']

        ## get product reference
        product_reference = soup.find('div', class_="product-reference text-muted").text.replace(' ', '')

        ## get product price
        products_price = soup.find('span', class_="product-price").text.replace(' ', '')

        ## get product image link
        product_img_div = soup.find('a', class_="thumbnail product-thumbnail")
        product_img = product_img_div.find('img')['data-src']

        ## get product availability
        product_availability = soup.find('div', class_="product-availability").text.strip()

        product = Product(product_name, product_reference, products_price, product_availability, product_img,
                          product_link)
        return product.toJSON()


###### ***************************api******************************

@app.get("/search")
def get_products():
    products = []
    if request.args.get('key'):
        key = request.args.get('key')

        ## get data from tunisianet
        html_text_tunisianet = search_tunisianet(key)
        soup_tun = BeautifulSoup(html_text_tunisianet, 'lxml')
        tunisianet_product = get_product_from_tunisianet(soup_tun)
        products.append(tunisianet_product)

        ## get data from wiki
        html_text_wiki = search_wiki(key)
        soup_wiki = BeautifulSoup(html_text_wiki, 'lxml')
        wiki_product = get_product_from_wiki(soup_wiki)
        products.append(wiki_product)

        ## get data from oxtek
        html_text_oxtek = search_oxtek(key)
        soup_oxtek = BeautifulSoup(html_text_oxtek, 'lxml')
        oxtek_product = get_product_from_oxtek(soup_oxtek)
        products.append(oxtek_product)

        return products


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
