import json 
import os
import sys
from loguru import logger

RAW = "/opt/airflow/data/raw"
FLAT = "/opt/airflow/data/flatten"

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
def flatten_data(run_date):
    try:
        logger.info("bat dau flatten")
        os.makedirs(FLAT,exist_ok=True)

        input_file = f"NEO_{run_date}.json"
        path = os.path.join(RAW,input_file)

        if not os.path.exists(path):
            raise Exception(f"File khong ton tai: {path}")

        with open(path, "r") as f:
            data = json.load(f)

        near_object = data["near_earth_objects"]
        flat_list = []

        for date in near_object:
            for asteroid in near_object[date]:
                asteroid["date"] = date
                flat_list.append(asteroid)
            
        output_file = os.path.join(FLAT, f"NEO_{run_date}_flattened.json")
        with open(output_file, "w") as f:
            json.dump(flat_list,f,indent=4)
        logger.success(f"flattened {run_date}\n------------------------------------------------------")

    except Exception as e:
        logger.exception(f"co loi {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_date = sys.argv[1]
    flatten_data(run_date)
