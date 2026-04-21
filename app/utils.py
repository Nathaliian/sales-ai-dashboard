import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "store_sales_data_cleaned.csv")

df = pd.read_csv(file_path)


def run_query(sql: str):
    try:
        sql = sql.lower()

        # TOTAL SALES
        if "sum(sales)" in sql and "group by" not in sql:
            total = df["sales"].sum()
            return pd.DataFrame([{"total_sales": total}])

        # GROUP BY
        match = re.search(r"group by ([a-z_]+)", sql)
        if match:
            col = match.group(1)

            if col in df.columns:
                result = df.groupby(col)["sales"].sum().reset_index()
                result.columns = [col, "total_sales"]
                return result

        # TOP N
        if "top" in sql:
            match = re.search(r"top (\d+)", sql)
            if match:
                n = int(match.group(1))
                return df.nlargest(n, "sales")[["product_name", "sales"]]

        return df.head(10)

    except Exception as e:
        return str(e)