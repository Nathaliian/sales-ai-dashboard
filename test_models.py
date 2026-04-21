import os
from dotenv import load_dotenv
from google import genai

# Load your .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: API Key not found in .env file!")
    exit()

# Initialize the Client
client = genai.Client(api_key=api_key)

print("--- LISTING ALL MODELS ---")
try:
    # Fetch the list of models
    models = client.models.list()
    
    # In the new SDK, 'models' is an iterable of model objects
    for model in models:
        # We just need the 'name' attribute
        print(f"✅ {model.name}")

except Exception as e:
    print(f"❌ Connection failed: {e}")