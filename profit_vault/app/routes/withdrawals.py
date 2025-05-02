from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Withdrawal, User
from datetime import datetime

withdrawals_bp = Blueprint('withdrawals', __name__, url_prefix='/api/withdrawals')

@withdrawals_bp.route('/request', methods=['POST'])
@jwt_required()
def request_withdrawal():
    data = request.json
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    amount = float(data['amount'])
    fee = amount * 0.02  # Example: 2% fee

    if user.balance < (amount + fee):
        return jsonify({'msg': 'Insufficient balance'}), 400

    withdrawal = Withdrawal(
        user_id=user.id,
        network=data['network'],
        wallet_address=data['wallet_address'],
        amount=amount,
        fee=fee,
        status='pending',
        date_created=datetime.utcnow()
    )

    user.balance -= (amount + fee)
    db.session.add(withdrawal)
    db.session.commit()
    return jsonify({'msg': 'Withdrawal request submitted. Awaiting approval.'}), 201

@withdrawals_bp.route('/', methods=['GET'])
@jwt_required()
def list_user_withdrawals():
    user_id = get_jwt_identity()
    withdrawals = Withdrawal.query.filter_by(user_id=user_id).all()
    return jsonify([w.to_dict() for w in withdrawals]), 200
