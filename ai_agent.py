import os
from dotenv import load_dotenv

load_dotenv()  # подхватит переменные из .env
api_key = os.getenv("OPENAI_API_KEY")