# Placeholder for tasks like interest compounding, email sending, etc.

from app.models import db, Investment
from datetime import datetime

def process_investment_profits():
    active_investments = Investment.query.filter_by(is_active=True).all()
    for inv in active_investments:
        # Apply dummy profit calculation, could be replaced with a more complex strategy
        days_elapsed = (datetime.utcnow() - inv.start_date).days
        if days_elapsed > 0:
            profit = inv.amount_invested * 0.01 * days_elapsed  # 1% daily example
            inv.profit_earned = profit
    db.session.commit()
