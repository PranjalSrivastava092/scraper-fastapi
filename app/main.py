from fastapi import FastAPI, Header
from app.scraper import Scraper
from app.constants import BASE_URL
from app.scrape_settings import ScrapeSettings
from app.utils import validate_token

app = FastAPI()

@app.post("/scrape/")
def scrape_dentalstall(settings: ScrapeSettings, token: str = Header(...)):
    validate_token(token)
    page = 1
    scraper = Scraper(BASE_URL, proxies=settings.proxy)
    
    while True:
        if settings.max_pages and page > settings.max_pages:
            break
        try:
            items_left = scraper.scrape_page(page)
            if not items_left:
                break
        except Exception as e:
            return {"error": str(e)}
        page += 1
    
    scraper.save_to_json()
    scraper.notify_status()

    return {"message": "Scraping completed", "data_saved_to": "res.json"}
