import json

def get_best_product(response):
    products = json.loads(response)["results"]
    clean_products = filter(lambda p: p["stars"] is not None and p['price'] is not None, products)
    best_products = sorted(clean_products, key=lambda e: (e["stars"], e["price"]))
    if best_products:
        return best_products[0]
    else:
        return None
