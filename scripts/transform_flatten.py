import json 
import os
import sys
from loguru import logger

RAW = "/opt/airflow/data/raw"
FLAT = "/opt/airflow/data/flatten"

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
        logger.success(f"flattened {run_date}")

    except Exception as e:
        logger.warning(f"co loi {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_date = sys.argv[1]
    flatten_data(run_date)
