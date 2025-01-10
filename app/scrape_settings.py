from pydantic import BaseModel, validator
from urllib.parse import urlparse
from typing import Optional
from app.constants import DEFAULT_MAX_PAGES
from app.utils import is_valid_url

class ScrapeSettings(BaseModel):
    max_pages: Optional[int] = DEFAULT_MAX_PAGES
    proxy: Optional[str] = None      

    @validator("max_pages")
    def validate_max_pages(cls, value):
        if value is not None and value <= 0:
            raise ValueError("max_pages must be greater than 0")
        return value

    @validator("proxy")
    def validate_proxy(cls, value):
        if value is not None:
            return is_valid_url(value)
        return True
