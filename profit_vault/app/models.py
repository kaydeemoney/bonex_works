from app import db
from datetime import datetime

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    transaction_pin = db.Column(db.String(4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Investment Plan model
class InvestmentPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_amount = db.Column(db.Float, nullable=False)
    max_amount = db.Column(db.Float, nullable=False)
    period_in_days = db.Column(db.Integer, nullable=False)
    monthly_roi = db.Column(db.Float, nullable=False)
    annual_roi = db.Column(db.Float, nullable=False)

# User Investment model
class UserInvestment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('investment_plan.id'), nullable=False)
    amount_invested = db.Column(db.Float, nullable=False)
    profit_earned = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

# Deposit model
class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    network = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Withdrawal model
class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    wallet_address = db.Column(db.String(100), nullable=False)
    network = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Referral model
class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commission_earned = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, etc.
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
