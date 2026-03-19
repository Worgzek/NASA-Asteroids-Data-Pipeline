import json 
import os
import csv
import sys
from loguru import logger

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

def Transform(run_date):
    try:
        Output = f"/opt/airflow/data/processed/asteroids_{run_date}.csv"
        logger.info(f"Bat dau Transform {run_date}.JSON -> .CSV")
        os.makedirs("/opt/airflow/data/processed",exist_ok=True)

        input_file = f"NEO_{run_date}_flattened.json"
        path = os.path.join(FLAT, input_file)

        if not os.path.exists(path):
            raise Exception(f"File khong ton tai: {path}")        

        with open(path, "r") as f:
            data = json.load(f)

        rows = []
            
        for asteroids in data:
            diameter_min = asteroids["estimated_diameter"]["meters"]["estimated_diameter_min"]
            diameter_max = asteroids["estimated_diameter"]["meters"]["estimated_diameter_max"]
            

            close_date = None
            velocity = None
            miss_distance = None

            if asteroids["close_approach_data"]:
                approach = asteroids["close_approach_data"][0]
                close_date = approach["close_approach_date"]
                velocity = float(approach["relative_velocity"]["kilometers_per_second"])
                miss_distance = float(approach["miss_distance"]["kilometers"])
                
            if velocity is None or miss_distance is None:
                continue

            if diameter_max <= 0 or velocity <= 0 or miss_distance <= 0:
                continue               
                
            row = {
                "asteroid_id": asteroids["id"],
                "name": asteroids["name"],
                "absolute_magnitude": asteroids["absolute_magnitude_h"],
                "diameter_min_m": diameter_min,
                "diameter_max_m": diameter_max,
                "velocity_km_s": velocity,
                "miss_distance_km":miss_distance,
                "date": asteroids["date"]
                }

            rows.append(row)
        
        if not rows:
            logger.warning("No data to transform")
            raise Exception("No data")
        keys = rows[0].keys()

        with open(Output,"w",newline="") as f:
            writer = csv.DictWriter(f,fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
        logger.success(f"Transform thanh cong {run_date}\n------------------------------------------------------")

    except Exception as e:
        logger.exception(f"da co loi {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_date = sys.argv[1]
    Transform(run_date)