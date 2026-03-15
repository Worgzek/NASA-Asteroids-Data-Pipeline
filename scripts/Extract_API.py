import requests
import json
import os
from datetime import datetime, timedelta
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")

def extract_API():
    start_date = datetime(2026,2,15)
    end_date = datetime(2026,2,22)
    current = start_date

    os.makedirs("datas/raw",exist_ok=True)

    while current <= end_date:
        chunk_end = current + timedelta(days=6)
        if chunk_end > end_date:
            chunk_end = end_date
        url = "https://api.nasa.gov/neo/rest/v1/feed"

        params = {
            "start_date": current.strftime("%Y-%m-%d"),
            "end_date": chunk_end.strftime("%Y-%m-%d"),
            "api_key": API_KEY
        }

        reponse = requests.get(url, params=params)
        datas = reponse.json()
        filename = f"datas/raw/feed_{params['start_date']}_{params['end_date']}.json"
        with open (filename,"w") as f:
            json.dump(datas,f,indent=4)
        logger.info("Da luu", filename)

        current = chunk_end + timedelta(days=1)

if __name__ == "__main__":
    extract_API()
