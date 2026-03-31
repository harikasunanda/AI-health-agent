import pandas as pd
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

# -------------------------------
# Create Engine (SQLAlchemy)
# -------------------------------
def get_engine():
    """Create and return SQLAlchemy engine"""
    try:
        connection_string = (
             "mysql+pymysql://readonlyuser:hngadmin%401234@"
            "hng-data-lake-flexi.mysql.database.azure.com:3306/mrc_datapoints"
        )

        engine = create_engine(connection_string)

        return engine

    except Exception as e:
        logging.error(f"Engine Creation Error: {e}")
        return None


# -------------------------------
# Load Data
# -------------------------------
def load_data(limit=100):
    """
    Load consultation data from database
    """
    engine = None

    try:
        engine = get_engine()

        if engine is None:
            return pd.DataFrame()

        query = f"""
        SELECT 
            patient_id,
            patient_name,
            doctor_name,
            speciality,
            scheduled_at
        FROM info_consultation_raw_data_new
        WHERE _id IS NOT NULL
        LIMIT {limit}
        """

        df = pd.read_sql(query, engine)

        # Convert datetime safely
        df["scheduled_at"] = pd.to_datetime(df["scheduled_at"], errors="coerce")

        logging.info(f"Loaded {len(df)} records from database")

        return df

    except Exception as e:
        logging.error(f"Database Error: {e}")
        return pd.DataFrame()

    finally:
        if engine:
            engine.dispose()
            logging.info("Database engine disposed")