import requests
import json
import os
from datetime import datetime, timedelta
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")

def extract_API():
    try:
        logger.info("Bat dau Extract")

        start_date = datetime(2026,2,15)
        end_date = datetime(2026,2,22)
        current = start_date

        os.makedirs("data/raw",exist_ok=True)

        while current <= end_date:
            chunk_end = current + timedelta(days=7)
            if chunk_end > end_date:
                chunk_end = end_date
            url = "https://api.nasa.gov/neo/rest/v1/feed"

            params = {
                "start_date": current.strftime("%Y-%m-%d"),
                "end_date": chunk_end.strftime("%Y-%m-%d"),
                "api_key": API_KEY
            }

            reponse = requests.get(url, params=params)
            data = reponse.json()
            filename = f"data/raw/NEO_{params['start_date']}_{params['end_date']}.json"
            with open (filename,"w") as f:
                json.dump(data,f,indent=4)
            logger.success("Da luu thanh cong", filename)

            current = chunk_end + timedelta(days=1)

    except Exception as e:
        logger.warning(f"co loi xay ra {e}")

if __name__ == "__main__":
    extract_API()
