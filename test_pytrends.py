# from pytrends.request import TrendReq
# from app.services.scraper import scrape_tiktok_trends

# # Try a potentially invalid or emoji-laden product name
# keyword = "Ice Roller"

# try:
#     pt = TrendReq()
#     pt.build_payload([keyword], timeframe="now 7-d", geo="US")
#     df = pt.interest_over_time()
#     print(df)

# except Exception as e:
#     print(f"Keyword failed: {keyword}")
#     print("Error:", e)



# if __name__ == "__main__":
#     results = scrape_tiktok_trends()
#     print("TIKTOK RESULTS:", results)

import os
import pandas as pd
from pytrends.request import TrendReq

def test_pytrends_save():
    pytrends = TrendReq(hl='en-US', tz=360)
    batch = ["Golf Balls"]
    pytrends.build_payload(batch, timeframe='now 7-d', geo='')
    df = pytrends.interest_over_time()

    print(df.head())

    logs_dir = "./pytrends_logs"
    os.makedirs(logs_dir, exist_ok=True)

    filename = os.path.join(logs_dir, "test_batch.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"[Batch Test] Keywords: {batch}\n\n")
        f.write(df.to_string(index=True))
    print("[✓] File saved to:", filename)


test_pytrends_save()