import psycopg2
from loguru import logger
from dotenv import load_dotenv
import os
import sys
load_dotenv()
PASS = os.getenv("PASS")

def log_ETL(run_id, step, status, records_processed, message):
    try:
        run_id = int(run_id.replace("-", ""))

        conn = None
        cur = None

        conn = psycopg2.connect(
            host="postgres",
            database= "nasa_neo",
            user= "airflow",
            password = PASS
            )
        cur = conn.cursor()
        cur.execute('''
                insert into etl_log(run_id,step,status,row_processed,message)
                values
                (%s, %s, %s, %s, %s)
                ''',(run_id, step, status, records_processed, message))
        conn.commit()
    except Exception as e:
        logger.exception(f'da co loi xay ra {e}')
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()
        logger.info('da dong ket noi')
    