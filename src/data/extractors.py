import pandas as pd
import sqlalchemy
from src.utils.config import load_config

class DataExtractor:
    def __init__(self):
        self.config = load_config()
        self.engine = sqlalchemy.create_engine(self.config['db_url'])

    def extract_from_sql(self, query):
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"Error extracting data: {e}")
            return pd.DataFrame()

    def extract_from_api(self, endpoint):
        # Placeholder for API extraction logic
        pass
