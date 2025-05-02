from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def generate_tokens(identity):
    access_token = create_access_token(identity=identity, expires_delta=timedelta(days=1))
    refresh_token = create_refresh_token(identity=identity)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
