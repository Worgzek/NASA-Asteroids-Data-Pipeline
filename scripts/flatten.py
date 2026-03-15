import json 
import os
from loguru import logger

RAW = "datas/raw"
FLAT = "datas/flatten"

def flatten_data():
    try:

        os.makedirs(FLAT,exist_ok=True)

        for file in os.listdir(RAW):
            if not file.endswith(".json"):
                continue

            path = os.path.join(RAW,file)
            with open(path, "r") as f:
                data = json.load(f)
            near_object = data["near_earth_objects"]
            flat_list = []
            for date in near_object:
                for asteroid in near_object[date]:
                    asteroid["date"] = date
                    flat_list.append(asteroid)
            
            output_file = os.path.join(FLAT, f"flat_{file}")
            with open(output_file, "w") as f:
                json.dump(flat_list,f,indent=4)
            logger.info(f"flattened {file}")

    except Exception as e:
        logger.warning(f"co loi {e}")

if __name__ == "__main__":
    flatten_data()