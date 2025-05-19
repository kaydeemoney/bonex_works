from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Investment, InvestmentPlan
from datetime import datetime, timedelta

investments_bp = Blueprint('investments', __name__, url_prefix='/api/investments')

@investments_bp.route('/', methods=['GET'])
@jwt_required()
def list_user_investments():
    user_id = get_jwt_identity()
    investments = Investment.query.filter_by(user_id=user_id).all()
    return jsonify([i.to_dict() for i in investments]), 200

@investments_bp.route('/create', methods=['POST'])
@jwt_required()
def create_investment():
    data = request.json
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    plan = InvestmentPlan.query.get(data['plan_id'])
    amount = float(data['amount'])

    if not plan or amount < plan.min_amount or amount > plan.max_amount:
        return jsonify({'msg': 'Invalid plan or amount'}), 400

    if user.balance < amount:
        return jsonify({'msg': 'Insufficient balance'}), 400

    end_date = datetime.utcnow() + timedelta(days=plan.period_in_days)
    investment = Investment(user_id=user.id, plan_id=plan.id, amount_invested=amount,
                            profit_earned=0.0, start_date=datetime.utcnow(),
                            end_date=end_date, is_active=True)

    user.balance -= amount
    db.session.add(investment)
    db.session.commit()
    return jsonify({'msg': 'Investment created successfully'}), 201
