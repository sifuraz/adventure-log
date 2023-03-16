from dotenv import load_dotenv
from pathlib import Path
import os

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
static = StaticFiles(directory=str(Path(BASE_DIR, "static")))
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

load_dotenv()

db_string = os.getenv("DATABASE_URL")
redis_url = os.getenv("REDIS_URL")
jwt_secret = os.getenv("JWT_SECRET")
