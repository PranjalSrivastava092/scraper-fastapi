import redis
import requests
import os
import json
from urllib.parse import urlparse
from fastapi import HTTPException, status, Query, Depends
from app.constants import STATIC_TOKEN, REDIS_DB, REDIS_HOST, REDIS_PORT


r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def validate_token(token: str = Depends(Query(...))):
    if token != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )

# Got this from here https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def download_image(image_url):
    if image_url == "N/A":
        return "N/A"
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image_name = os.path.basename(urlparse(image_url).path)
        image_path = os.path.join("images", image_name)
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return image_path
    except Exception as e:
        return "N/A"

def parse_price(price_str):
    try:
        return float(price_str.replace("₹", "").replace(",", ""))
    except ValueError:
        return 0.0

def is_product_price_changed(product_name, current_price):
    cached_product = r.get(product_name)
    if cached_product:
        cached_data = json.loads(cached_product)
        cached_price = cached_data.get("price")
        return cached_price != current_price 
    return True

def cache_product(product_name, price, image_path):
    product_data = {
        "price": price,
        "image_path": image_path
    }
    r.set(product_name, json.dumps(product_data))