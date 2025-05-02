from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Deposit, User
from datetime import datetime

deposits_bp = Blueprint('deposits', __name__, url_prefix='/api/deposits')

@deposits_bp.route('/request', methods=['POST'])
@jwt_required()
def request_deposit():
    data = request.json
    user_id = get_jwt_identity()

    deposit = Deposit(
        user_id=user_id,
        network=data['network'],
        amount=data['amount'],
        transaction_id=data['transaction_id'],
        status='pending',
        date_created=datetime.utcnow()
    )

    db.session.add(deposit)
    db.session.commit()
    return jsonify({'msg': 'Deposit request submitted. Awaiting approval.'}), 201

@deposits_bp.route('/', methods=['GET'])
@jwt_required()
def list_user_deposits():
    user_id = get_jwt_identity()
    deposits = Deposit.query.filter_by(user_id=user_id).all()
    return jsonify([d.to_dict() for d in deposits]), 200
