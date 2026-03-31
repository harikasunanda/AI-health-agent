import mysql.connector
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def get_connection():
    """Create and return DB connection"""
    return mysql.connector.connect(
        host="hng-data-lake-flexi.mysql.database.azure.com",
        user="readonlyuser",
        password="hngadmin@1234",
        database="mrc_datapoints",
        port=3306
    )

def load_data(limit=100):
    """
    Load consultation data from database
    """
    conn = None
    try:
        conn = get_connection()

        query = """
        SELECT 
            _id,
            doctor_name,
            speciality,
            scheduled_at
        FROM info_consultation_raw_data
        WHERE application_id IS NOT NULL
        LIMIT %s
        """

        df = pd.read_sql(query, conn, params=(limit,))

        df["scheduled_at"] = pd.to_datetime(df["scheduled_at"], errors="coerce")

        logging.info(f"Loaded {len(df)} records from database")

        return df

    except mysql.connector.Error as db_err:
        logging.error(f"MySQL Error: {db_err}")
        return pd.DataFrame()

    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return pd.DataFrame()

    finally:
        if conn and conn.is_connected():
            conn.close()
            logging.info("Database connection closed")