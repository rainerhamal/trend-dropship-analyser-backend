import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_with_gpt(chart_data):
    # Step 1: Create scores based on interest
    opportunities = []
    for item in chart_data:
        name = item["name"]
        avg = item["average"]
        values = item["values"]
        dates = item["dates"]

        # Normalize average to 0–100 scale (safe rounding)
        score = min(round(avg), 100)

        opportunities.append({
            "name": name,
            "score": score,
            "niche": "Unknown",         # Let GPT/niche classifier fill this later
            "source": "Google Trends",  # Source of trend info
            "interest_values": values,  # Needed for frontend charts
            "dates": dates,
        })

    # Step 2: Summarize trends using GPT
    trend_summary_text = "\n".join([
        f"{item['name']} — Avg: {item['average']}, Interest: {item['values']}"
        for item in chart_data
    ])

    prompt = f"""
                You are a product trend analyst AI.

                Based on the following Google Trends 7-day interest data for various products, provide a short analytical summary including:
                - Overall market trend patterns
                - Which types of products appear to be rising
                - Actionable advice for researchers or marketers

                Only return the summary. No bullets or lists.

                Product Trend Data:         
                {trend_summary_text}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        summary = content.strip() if content else "No summary returned by GPT."
    except Exception as e:
        print("[!] GPT failed to generate summary:", e)
        summary = "No summary available due to GPT error."

    return summary, opportunities
