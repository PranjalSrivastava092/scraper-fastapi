import requests
import json
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, base_url, proxies=None):
        self.base_url = base_url
        self.proxies = proxies
        self.scraped_data = []

    def scrape_page(self, page):
        url = f"{self.base_url}"
        try:
            response = requests.get(url, proxies=self.proxies, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            raise Exception(f"Failed to fetch page {page}")

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select(".product-inner")

        if not products:
            return False

        for product in products:
            name = product.select_one("img")['alt'] if product.select_one("img") else "N/A"
            price = product.select_one(".price .woocommerce-Price-amount bdi").text.strip() if product.select_one(".price .woocommerce-Price-amount bdi") else "N/A"
            image_url = product.select_one("img")['data-lazy-src'] if product.select_one("img") else "N/A"

            self.scraped_data.append({
                "product_title": name.split(' -')[0].strip(),
                "product_price": self.parse_price(price),
                "path_to_image": image_url,
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
    
    def parse_price(self, price_str):
        try:
            return float(price_str.replace("₹", "").replace(",", ""))
        except ValueError:
            return 0.0
