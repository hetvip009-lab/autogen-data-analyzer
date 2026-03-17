from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
client = genai.Client(api_key=api_key)

# Test connection
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say Hello! I am AutoGen Data Analyzer!"
)

print(response.text)