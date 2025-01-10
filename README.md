# scraper-fastapi

A FastAPI based webscraper.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.7+**
- **Redis** server running locally or remotely

## Installation

Follow these steps to set up the project:

### 1. Clone the Repository

git clone https://github.com/your-username/web-scraping-fastapi.git
cd web-scraping-fastapi

### 2. Install Dependencies

Install the required Python packages listed in the requirements.txt file:
pip install -r requirements.txt

### 3. Running the application

To run the app, use:
uvicorn main:app --reload
This will start the FastAPI server at http://127.0.0.1:8000.

### 4. API Endpoint

POST /scrape

Request Body:
max_pages: Optional. Limit the number of pages to scrape.
proxy: Optional. Should be a string.

Request Headers:
token: Required. Pass the static token for authentication. You can modify the static access token in `app/constants.py`.
