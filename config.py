import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 365 * 24 * 60 * 60  # Token expired after 365 days
    SECURITY_ALGORITHM = 'HS256'
    USERNAME_AUTH = os.getenv('USERNAME_AUTH', '')
    PASSWORD_AUTH = os.getenv('PASSWORD_AUTH', '')
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')


settings = Settings()
