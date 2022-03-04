
import os
from dotenv import load_dotenv


if os.path.exists(".env"):
    load_dotenv()

QUEUE_NAME = os.getenv("QUEUE_NAME", "mairror")
NUM_MESSAGES = int(os.getenv("NUM_MESSAGES", "1"))
WAIT_TIME_SECONDS = int(os.getenv("WAIT_TIME_SECONDS", "10"))
