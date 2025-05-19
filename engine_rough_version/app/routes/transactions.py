from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Deposit, Withdrawal, Investment, ReferralBonus
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    tx_type = request.args.get('type')
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    filters = {
        'deposit': Deposit,
        'withdrawal': Withdrawal,
        'investment': Investment,
        'referral': ReferralBonus
    }

    if tx_type not in filters:
        return jsonify({'msg': 'Invalid transaction type'}), 400

    model = filters[tx_type]
    query = model.query.filter_by(user_id=user_id)

    if from_date and to_date:
        query = query.filter(model.date_created.between(from_date, to_date))

    return jsonify([t.to_dict() for t in query.all()]), 200
