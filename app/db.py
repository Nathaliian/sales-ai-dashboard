import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load .env from root folder
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get DB connection string
connection_string = os.getenv("DB_CONNECTION_STRING")

# Debug (temporary - remove later)
print("DB CONNECTION STRING:", connection_string)

# Create engine
engine = create_engine(connection_string)

# Test connection (optional but useful)
try:
    conn = engine.connect()
    print("✅ Database connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Database connection failed:", e)