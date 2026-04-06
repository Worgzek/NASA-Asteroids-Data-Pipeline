import requests
import json
import os
import sys
from datetime import datetime, timedelta
from loguru import logger
from dotenv import load_dotenv
from db_log import log_ETL
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY")
# Import libraries
run_date = sys.argv[1]
LOG_FILE = f"/opt/airflow/logs/pipeline_{run_date}.log"
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
#Logging

def extract_API(run_date):
    try:
        logger.info(f"Bat dau extract api ngay {run_date}")
        os.makedirs("/opt/airflow/data/raw",exist_ok=True)

        url = "https://api.nasa.gov/neo/rest/v1/feed"     
        params = {
            "start_date": run_date,
            "end_date": run_date,
            "api_key": API_KEY
        }

        response = requests.get(url, params=params, timeout=120)
        if response.status_code != 200:
            raise Exception(f"lay api khong thanh cong: {response.status_code}")
        data = response.json()

        filename = f"/opt/airflow/data/raw/NEO_{run_date}.json"

        with open (filename,"w") as f:
            json.dump(data,f,indent=4)
        logger.success(f"Da luu thanh cong {filename}\n------------------------------------------------------")
        
        log_ETL(run_date, "extract", "success", None, f"Da luu thanh cong {filename}")


    except Exception as e:
        logger.exception(f"co loi xay ra {e}")
        log_ETL(run_date, "extract", "failed", None, f"co loi xay ra {e}")

        sys.exit(1)


if __name__ == "__main__":
    extract_API(run_date)