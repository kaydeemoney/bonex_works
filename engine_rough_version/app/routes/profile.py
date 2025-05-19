from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/view', methods=['GET'])
@jwt_required()
def view_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile": user.mobile,
            "gender": user.gender,
            "country": user.country,
            "state": user.state,
        }), 200
    return jsonify(message="User not found"), 404

@profile_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.mobile = data.get('mobile', user.mobile)
        user.gender = data.get('gender', user.gender)
        user.country = data.get('country', user.country)
        user.state = data.get('state', user.state)
        db.session.commit()
        return jsonify(message="Profile updated successfully"), 200
    return jsonify(message="User not found"), 404
