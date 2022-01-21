import json
import requests
import re


def getQID(url):
    url_regex = re.compile(r'qid=(\d+)')
    mo = url_regex.search(url)
    qID = mo.groups()
    return qID


def get_best_product(response):
    loaded_response = json.loads(response)
    sponsored_products = loaded_response["ads"]
    other_products = loaded_response["results"]
    products = sponsored_products + other_products
    clean_products = filter(lambda p: p["stars"] is not None and p['price'] is not None, products)
    best_products = sorted(clean_products, key=lambda e: (e["stars"], e["price"]))
    if best_products:
        return best_products[0]
    else:
        return None
