import requests
import json
import os
import time
from bs4 import BeautifulSoup
from app.constants import DEFAULT_DELAY, DEFAULT_RETRIES
from app.utils import is_valid_url, is_product_price_changed, cache_product, download_image, parse_price

class Scraper:
    def __init__(self, base_url, proxies=None):
        self.base_url = base_url
        self.proxies = proxies
        self.scraped_data = []

    def scrape_page(self, page, retries=DEFAULT_RETRIES, delay=DEFAULT_DELAY):
        url = self.base_url if page == 1 else f"{self.base_url}page/{page}/"
        for attempt in range(retries):
            try:
                response = requests.get(url, proxies=self.proxies, timeout=10)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1}: Retrying page {page} in {delay} seconds")
                    time.sleep(delay)
                else:
                    raise Exception(f"Failed to fetch page {page} after {retries} attempts: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select(".product-inner")

        if not products:
            return False

        for product in products:
            name = product.select_one("img")['alt'] if product.select_one("img") else "N/A"
            price = product.select_one(".price .woocommerce-Price-amount bdi").text.strip() if product.select_one(".price .woocommerce-Price-amount bdi") else "N/A"
            image_url = product.select_one("img")['data-lazy-src'] if product.select_one("img") else "N/A"

            if not is_valid_url(image_url):
                image_url = "N/A"

            image_path = download_image(image_url)

            if not is_product_price_changed(name, price):
                print(f"Skipping update for {name}, price not changed.")
                continue

            cache_product(name, price, image_path)

            self.scraped_data.append({
                "product_title": name.split(' -')[0].strip(),
                "product_price": parse_price(price),
                "path_to_image": image_path,
            })

        return True
    
    def save_to_json(self, file_name="data/res.json"):
        try:
            with open(file_name, "w") as file:
                json.dump(self.scraped_data, file, indent=4)
        except Exception as e:
            print(f"Error saving data to {file_name}: {e}")

    def notify_status(self):
        print(f"Scraping completed. Total products scraped: {len(self.scraped_data)}")
    
