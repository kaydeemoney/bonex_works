import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql://user:pass@localhost/profit_vault")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret")
