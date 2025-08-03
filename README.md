<<<<<<< HEAD
# Trend Dropship Analyser Backend

This application is a backend service for analyzing trending products across major e-commerce and social platforms. It uses web scraping, Google Trends, and GPT-4 to provide actionable insights for dropshipping and product research.

## Features
- Scrapes trending products from Amazon, AliExpress, and TikTok
- Fetches Google Trends data for product keywords
- Uses GPT-4 to generate analytical summaries of product trends
- REST API built with FastAPI
- CORS enabled for frontend integration

## Technologies Used
- Python 3.11+
- FastAPI
- Selenium & undetected-chromedriver
- BeautifulSoup
- pytrends
- OpenAI GPT-4 API
- dotenv

## Setup Instructions
1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd trend-dropship-analyser-backend
   ```
2. **Create and activate a virtual environment**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Copy `.env.example` to `.env` and add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
5. **Install ChromeDriver**
   - Download and install ChromeDriver compatible with your Chrome version.
   - Ensure it is in your PATH or specify its location in the code if needed.

## Running the Application
```sh
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000/api`.

## API Endpoints
- `/api/analyze` — Analyze trending products and get GPT-4 summary
- `/api/trends` — Get combined trending keywords

## Notes
- Scraping Amazon, AliExpress, and TikTok may require anti-bot measures and may break if site structures change.
- Google Trends API (pytrends) has rate limits and keyword restrictions.
- GPT-4 API usage may incur costs.

## License
MIT License

## Author
Rainer Hamal
=======
# ⚙️ TrendOps API – FastAPI Backend

This is the backend service for https://github.com/rainerhamal/trend-dropship-analyser, a trend analysis platform powered by FastAPI. It handles incoming analysis requests, processes data (e.g., from Google Trends), and returns structured insights for frontend visualization.

---

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI** – Web framework
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation
- **CORS Middleware** – For frontend-backend communication

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/rainerhamal/trend-dropship-analyser-backend/new/main?filename=README.md.git

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```
>>>>>>> 0701c3e56da41117c15e987817a23d865157c04f
