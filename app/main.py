from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scraper import Scraper
from typing import Optional

app = FastAPI()

class ScrapeSettings(BaseModel):
    max_pages: Optional[int] = 3
    proxy: Optional[str] = None

@app.post("/scrape/")
def scrape_catalogue(settings: ScrapeSettings):
    base_url = "https://dentalstall.com/shop/"
    page = 1
    scraper = Scraper(base_url, proxies=settings.proxy)
    
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
