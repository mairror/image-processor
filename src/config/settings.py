import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

QUEUE_NAME = os.getenv("QUEUE_NAME", "mairror")
NUM_MESSAGES = int(os.getenv("NUM_MESSAGES", "1"))
WAIT_TIME_SECONDS = int(os.getenv("WAIT_TIME_SECONDS", "10"))
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_PATH = os.getenv("API_PATH", "/images/faces")
API_KEY = os.getenv("API_KEY", "test")
API_KEY_HEADER = os.getenv("API_KEY_HEADER", "X-Api-Key")
