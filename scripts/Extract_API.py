import requests
import json
import os
import sys
from datetime import datetime, timedelta
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")

def extract_API(run_date):
    try:
        logger.info(f"Bat dau Extract ngay {run_date}")
        os.makedirs("/opt/airflow/data/raw",exist_ok=True)

        url = "https://api.nasa.gov/neo/rest/v1/feed"     
        params = {
            "start_date": run_date,
            "end_date": run_date,
            "api_key": API_KEY
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API failed: {response.status_code}")
        data = response.json()

        filename = f"/opt/airflow/data/raw/NEO_{run_date}.json"
        with open (filename,"w") as f:
            json.dump(data,f,indent=4)
        logger.success("Da luu thanh cong", filename)

    except Exception as e:
        logger.warning(f"co loi xay ra {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_date = sys.argv[1] if len(sys.argv) > 1 else None
    extract_API(run_date)
