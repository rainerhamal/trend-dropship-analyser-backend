import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from pytrends.request import TrendReq
import statistics
from typing import List
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
import random
import re
import os

def _get_driver():
    options = uc.ChromeOptions()
    # Temporarily disable headless for debugging
    # options.add_argument("--headless")  # Uncomment only after it works
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled") 

    return uc.Chrome(options=options)

def scrape_amazon_top_products(limit: int = 20) -> List[str]:
    print("[✓] Scraping Amazon: Best Sellers...")
    url = "https://www.amazon.com/Best-Sellers/zgbs"

    driver = _get_driver()
    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.p13n-sc-truncate-desktop-type2, div.p13n-sc-truncate, div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1"))
        )
    except Exception as e:
        print("[!] Timeout waiting for bestseller list to load.")
        driver.save_screenshot("amazon_timeout.png")
        with open("amazon_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        return []

    # Save debug info
    driver.save_screenshot("amazon_loaded.png")
    with open("amazon_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    print("[✓] Extracting product titles...")

    titles = soup.select("div.p13n-sc-truncate-desktop-type2, div.p13n-sc-truncate, div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
    products = [t.get_text(strip=True) for t in titles if t.get_text(strip=True)]   
    print(f"[✓] Found {len(products)} products.")
    return products[:limit]

# def scrape_aliexpress_bestsellers() -> List[str]:
#     url = "https://www.aliexpress.com/category/100003109/women-clothing.html?g=y&SortType=total_tranpro_desc"
#     driver = _get_driver()
#     driver.get(url)
#     time.sleep(7)
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     driver.quit()

#     titles = soup.select("a.product-title")
#     products = [t.get_text(strip=True) for t in titles if t.get_text(strip=True)]

#     return products[:10]

# def scrape_tiktok_trends() -> list[str]:
#     print("[✓] Launching browser...")
#     options = uc.ChromeOptions()
#     options.add_argument("--headless=new")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--window-size=1920,1080")

#     driver = uc.Chrome(options=options)
#     driver.get("https://www.tiktok.com/tag/tiktokmademebuyit")

#     # Scroll multiple times to load more content
#     scroll_pause_time = 3
#     for i in range(5):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)

#     # Let TikTok fully load (extra buffer)
#     time.sleep(5)

#     # Save raw HTML for inspection
#     html = driver.page_source
#     with open("tiktok_debug.html", "w", encoding="utf-8") as f:
#         f.write(html)
#     print("[✓] Saving HTML...")

#     # Parse with BeautifulSoup
#     soup = BeautifulSoup(html, "html.parser")
#     print("[✓] Extracting text from spans/divs...")

#     # Try extracting from spans or other tags containing text
#     items = []
#     for tag in soup.find_all(["span", "h3", "a", "strong", "p"]):
#         text = tag.get_text(strip=True)
#         if 5 < len(text) < 60 and not any(x in text.lower() for x in ["tiktok", "login", "search", "for you", "explore"]):
#             items.append(text)

#     # Deduplicate and return top 10 cleaned results
#     final_products = list(dict.fromkeys(items))[:10]
#     print("RAW EXTRACTED ITEMS:", final_products)
#     driver.quit()
#     return final_products

def scrape_amazon_with_retries(max_retries=3):
    for attempt in range(max_retries):
        try:
            return scrape_amazon_top_products()
        except WebDriverException as e:
            print(f"[!] Attempt {attempt+1} failed:", e)
            time.sleep(random.uniform(2, 5))
    return []

def get_combined_trending_keywords() -> List[str]:
    products = []

    try:
        products += scrape_amazon_with_retries()
    except Exception as e:
        print("[!] Amazon scrape failed after retries:", e)

    # try:
    #     products += scrape_aliexpress_bestsellers()
    # except Exception as e:
    #     print("[!] AliExpress scrape failed:", e)

    # try:
    #     products += scrape_tiktok_trends()
    # except Exception as e:
    #     print("[!] TikTok scrape failed:", e)

    # Remove duplicates, strip extra spaces, and return top 10
    print("[RAW PRODUCTS]:", products)
    cleaned = [
        p.strip()
        for p in products
        if isinstance(p, str) and 5 <= len(p.strip()) <= 100
    ]

    unique_products = list(dict.fromkeys(cleaned))
    print("[FINAL PRODUCTS]:", unique_products)
    return unique_products[:10]
    # return ["Ice Roller", "Mini Printer", "Portable Blender", "Water Flosser", "Standing Desk"]

def fetch_interest_over_time(keywords: List[str]):
    import re
    pytrends = TrendReq(hl='en-US', tz=360)
    chart_data = []
    batch_size = 5

    # Create logs directory at root
    logs_dir = os.path.join(os.getcwd(), "pytrends_logs")
    os.makedirs(logs_dir, exist_ok=True)

    def is_valid_kw(kw):
        return (
            isinstance(kw, str)
            and 2 <= len(kw) <= 100
            and not re.search(r"[^\w\s\-\'&.,]", kw)  # allow &, ., , in addition
        )

    # Clean keywords
    clean_keywords = [kw.strip() for kw in keywords if is_valid_kw(kw.strip())]
    print("[CLEANED KEYWORDS]:", clean_keywords)

    for i in range(0, len(clean_keywords), batch_size):
        batch = clean_keywords[i:i + batch_size]
        try:
            pytrends.build_payload(batch, timeframe='now 7-d', geo='')
            df = pytrends.interest_over_time()

            # Save full DataFrame to file
            batch_filename = os.path.join(logs_dir, f"pytrends_batch_{i//batch_size + 1}.txt")
            with open(batch_filename, "w", encoding="utf-8") as f:
                f.write(f"[Batch {i//batch_size + 1}] Keywords: {batch}\n\n")
                f.write(df.to_string(index=True))
            print(f"[✓] Saved batch {i//batch_size + 1} to {batch_filename}")

            if df.empty or not any(col in df.columns for col in batch):
                print(f"[!] No data for batch {batch}")
                continue

            for keyword in batch:
                if keyword not in df.columns:
                    continue
                values = df[keyword].tolist()
                dates = pd.to_datetime(df.index).strftime("%Y-%m-%d").tolist()
                avg = round(statistics.mean(values), 2)

                chart_data.append({
                    "name": keyword,
                    "values": values,
                    "dates": dates,
                    "average": avg
                })

        except Exception as e:
            print(f"[!] Error with batch {batch}: {e}")
            continue

    return chart_data
