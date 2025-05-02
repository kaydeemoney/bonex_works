from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ReferralBonus

referrals_bp = Blueprint('referrals', __name__, url_prefix='/api/referrals')

@referrals_bp.route('/bonuses', methods=['GET'])
@jwt_required()
def referral_bonuses():
    user_id = get_jwt_identity()
    bonuses = ReferralBonus.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in bonuses]), 200
