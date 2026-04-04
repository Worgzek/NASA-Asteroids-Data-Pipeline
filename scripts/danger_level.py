import psycopg2
from psycopg2.extras import execute_values
import os
import sys
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

PASS = os.getenv("PASS")

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

def danger_score():
    conn = None
    cur = None
    try:
        logger.info("dang ket noi Database")

        conn = psycopg2.connect(
            host="postgres",
            database= "nasa_neo",
            user= "airflow",
            password = PASS
            )
        cur = conn.cursor()

        logger.info("bat dau tao bang")
        cur.execute("""
            create table if not exists danger_score(
                asteroid_id BIGINT Primary Key,
                name VARCHAR(30),
                diameter_max_m FLOAT,
                velocity_km_s FLOAT,
                miss_distance_km FLOAT,  
                risk_score FLOAT,
                danger_level VARCHAR(10),                            
                date TIMESTAMP,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                primary key(asteroid_id, date)
                    )
            """)
        logger.info("thuc hien task")
        query = """
            SELECT
                asteroid_id,
                name,
                diameter_max_m,
                velocity_km_s,
                miss_distance_km,
                risk_score,
                
                CASE
                    WHEN risk_score >= 8 THEN 'EXTREME'
                    WHEN risk_score >= 6 THEN 'HIGH'
                    WHEN risk_score >= 4 THEN 'MEDIUM'
                    ELSE 'LOW'
                END AS danger_level,
                date

            FROM (
                SELECT 
                    asteroid_id,
                    name,
                    diameter_max_m,
                    velocity_km_s,
                    miss_distance_km,

                    (
                        (diameter_max_m / 1000.0) * 4 +
                        (velocity_km_s / 30.0) * 3 +
                        LEAST(7500000.0 / NULLIF(miss_distance_km,0), 1) * 3
                    ) AS risk_score,

                    date

                FROM Asteroids
            ) as sub

            ORDER BY risk_score DESC;
            """
        cur.execute(query)
        results = cur.fetchall()
        logger.info("Load data vao bang danger_score")
        insert_query = """
            insert into danger_score(asteroid_id, name, diameter_max_m, velocity_km_s, miss_distance_km, risk_score, danger_level, date)
            values %s
            on conflict(asteroid_id) do update set
                name = excluded.name,
                diameter_max_m = excluded.diameter_max_m,
                velocity_km_s = excluded.velocity_km_s,
                miss_distance_km = excluded.miss_distance_km,
                risk_score = excluded.risk_score,
                danger_level = excluded.danger_level,
                date = excluded.date,
                last_updated = current_timestamp;
            """
        execute_values(cur,insert_query,results)
        conn.commit()
        logger.success(f"da fetch thanh cong {len(results)} dong\n------------------------------------------------------")
        sys.exit(0)

    except Exception as e:
        logger.exception(f"da co loi xay ra {e}")
        if conn:
            conn.rollback()
        sys.exit(1)

    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()
if __name__ == "__main__":
    danger_score()


