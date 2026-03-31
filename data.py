import pandas as pd
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

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


def load_data(limit=100):
    """
    Load patient consultation data from database
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
            patient_age,
            patient_gender,
            height,
            weight,
            bmi,
            systolic_bp,
            diastolic_bp,
            pulse,
            spo2,
            temperature,
            respiratoryRate,
            doctorsymptoms,
            diagnosis,
            labtestresult
        FROM info_consultation_raw_data_new
        WHERE application_id IS NOT NULL

        LIMIT {limit}
        """

        df = pd.read_sql(query, engine)

        df.columns = df.columns.str.strip().str.lower()

        numeric_cols = [
            "height", "weight", "bmi",
            "systolic_bp", "diastolic_bp",
            "pulse", "spo2", "temperature",
            "respiratoryrate"
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        logging.info(f"Loaded {len(df)} records from database")

        return df

    except Exception as e:
        logging.error(f"Database Error: {e}")
        return pd.DataFrame()

    finally:
        if engine:
            engine.dispose()
            logging.info("Database engine disposed")