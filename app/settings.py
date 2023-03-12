from dotenv import load_dotenv
import os

load_dotenv()

db_string = os.getenv("DATABASE_URL")
