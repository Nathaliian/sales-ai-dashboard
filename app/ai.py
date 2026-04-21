import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1"}
)


def generate_sql(question: str):
    prompt = f"""
You are an expert SQL generator.

Database: SQL Server

Table: dbo.store_sales_data_cleaned

COLUMNS:
customer_id, customer_name, last_name, date_of_birth,
sales, year, outlet_type, city_type, category_of_goods,
region, country, segment, sales_date, order_id, order_date,
ship_date, ship_mode, state, postal_code, product_id,
sub_category, product_name, quantity, discount, profit,
shipping_days, age, Age_Group

RULES:
- ALWAYS use dbo.store_sales_data_cleaned
- ONLY use given columns
- NEVER invent names
- Use SQL Server syntax (TOP, not LIMIT)
- ALWAYS use aliases (AS)

Examples:
- total sales → SELECT SUM(sales) AS total_sales FROM dbo.store_sales_data_cleaned
- sales by region → SELECT region, SUM(sales) AS total_sales FROM dbo.store_sales_data_cleaned GROUP BY region

Question: {question}

Return ONLY SQL.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    print("SQL:", sql)

    return sql


def explain_result(question, df):
    try:
        data_sample = df.head(10).to_string()

        prompt = f"""
You are a business analyst.

User question:
{question}

Query result:
{data_sample}

Give a short business insight (2 lines max).
Mention key numbers clearly.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Insight error: {str(e)}"