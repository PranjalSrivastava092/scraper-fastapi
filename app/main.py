from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scraper import Scraper
from typing import Optional

app = FastAPI()

class ScrapeSettings(BaseModel):
    max_pages: Optional[int] = 1
    proxy: Optional[str] = None

@app.post("/scrape/")
def scrape_catalogue(settings: ScrapeSettings):
    base_url = "https://dentalstall.com/shop/"
    scraper = Scraper(base_url, proxies=settings.proxy)
    
    scraper.scrape_page(1)
    scraper.save_to_json()
    scraper.notify_status()

    return {"message": "Scraping completed", "data_saved_to": "res.json"}
