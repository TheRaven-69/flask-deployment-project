import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "data.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/static/img')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024