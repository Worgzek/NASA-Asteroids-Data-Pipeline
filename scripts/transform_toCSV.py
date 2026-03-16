import json 
import os
import csv
from loguru import logger

FLAT = "data/flatten"
Output = "data/processed/asteroids.csv"

def Transform():
    try:
        logger.info("Bat dau Transform .JSON -> .CSV")
        os.makedirs("data/processed",exist_ok=True)
        rows = []
        for file in os.listdir(FLAT):
            if not file.endswith(".json"):
                continue
            path = os.path.join(FLAT, file)
            with open(path, "r") as f:
                data = json.load(f)
            
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
            return
        keys = rows[0].keys()

        with open(Output,"w",newline="") as f:
            writer = csv.DictWriter(f,fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
        logger.success("Transform thanh cong")


    except Exception as e:
        logger.warning(f"da co loi {e}")

if __name__ == "__main__":
    Transform()