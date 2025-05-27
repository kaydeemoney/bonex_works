# config.py
import os
#using secret key to protect my input
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bonex1:bonexproject@localhost/new_profit_vault'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '7caa483b-e1c7-4a65-b901-queenofthecoast'
