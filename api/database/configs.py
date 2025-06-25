import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "57678")
DATABASE_NAME = os.getenv("DATABASE_NAME", "qc")

POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", 10))
MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", 20))
POOL_TIMEOUT = int(os.getenv("DATABASE_POOL_TIMEOUT", 30))
POOL_RECYCLE = int(os.getenv("DATABASE_POOL_RECYCLE", 3600))
