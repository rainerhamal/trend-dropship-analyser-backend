from fastapi import APIRouter
from app.services.scraper import get_combined_trending_keywords, fetch_interest_over_time
from app.services.analyser import analyze_with_gpt
from fastapi import FastAPI

router = APIRouter()


@router.post("/analyse")
async def run_analysis():
    keywords = get_combined_trending_keywords()
    trend_data = fetch_interest_over_time(keywords)
    summary, opportunities = analyze_with_gpt(trend_data)
    return {
        "chartData": trend_data,
        "summary": summary,
        "opportunities": opportunities,
    }
