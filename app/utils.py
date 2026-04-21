import pandas as pd
from app.db import engine

def run_query(sql):
    try:
        # basic safety check
        if "delete" in sql.lower():
            return "Dangerous query blocked"

        df = pd.read_sql(sql, engine)
        return df

    except Exception as e:
        return str(e)