# ⚙️ TrendOps API – FastAPI Backend

This is the backend service for https://github.com/rainerhamal/trend-dropship-analyser, a trend analysis platform powered by FastAPI. It handles incoming analysis requests, processes data (e.g., from Google Trends), and returns structured insights for frontend visualization.

---

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI** – Web framework
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation
- **HTTPX / aiohttp** (if used) – For async HTTP requests
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
