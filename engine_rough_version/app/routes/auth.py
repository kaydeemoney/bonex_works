from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.utils.jwt_utils import create_access_token, create_refresh_token, decode_jwt_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        mobile=data['mobile'],
        gender=data['gender'],
        country=data['country'],
        state=data['state'],
        password_hash=hashed_password,
        transaction_pin=data['transaction_pin']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User created successfully"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter((User.email == data['email']) | (User.mobile == data['mobile'])).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify(message="Invalid credentials"), 401
