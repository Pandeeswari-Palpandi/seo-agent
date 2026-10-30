import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. Please add it to your .env file."
    )

LLM_CONFIG = {
    "model": "gpt-4.1-mini",
    "api_key": OPENAI_API_KEY,
}
