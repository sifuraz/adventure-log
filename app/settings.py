from dotenv import load_dotenv
import os

load_dotenv()

db_string = os.getenv("DATABASE_URL")
redis_url = os.getenv("REDIS_URL")
jwt_secret = os.getenv("JWT_SECRET")
