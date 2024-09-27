import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

SECRET_JWT = os.getenv("SECRET_JWT")
ENVIRONMENT = os.getenv("ENVIRONMENT")

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{quote(DATABASE_PASSWORD)}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
