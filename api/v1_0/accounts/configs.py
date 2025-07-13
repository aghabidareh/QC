from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
AUTHORIZE_URL = os.getenv("AUTHORIZE_URL")
