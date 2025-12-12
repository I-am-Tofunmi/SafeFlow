from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db import get_conn
from app.models import Transaction, User

router = APIRouter(prefix="/analytics", tags=["Analytics & Budgeting"])

# ---------------------------------------------------------
# 1. Financial Overview (Income vs Expense)
# ---------------------------------------------------------
@router.get("/spending-summary/{user_id}")
def get_spending_summary(user_id: int, db: Session = Depends(get_conn)):
    """
    Calculates total credits (income) vs debits (expenses)
    to show the user their cash flow.
    """
    # Sum of all credits (Money In)
    total_credit = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, 
                Transaction.transaction_type == 'credit',
                Transaction.status == 'completed').scalar() or 0.0

    # Sum of all debits (Money Out)
    total_debit = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, 
                Transaction.transaction_type == 'debit',
                Transaction.status == 'completed').scalar() or 0.0

    net_balance = total_credit - total_debit
    savings_rate = (net_balance / total_credit * 100) if total_credit > 0 else 0

    return {
        "user_id": user_id,
        "total_income": total_credit,
        "total_spent": total_debit,
        "net_balance": net_balance,
        "savings_rate_percentage": round(savings_rate, 1)
    }

# ---------------------------------------------------------
# 2. Smart Budgeting Nudge (The "SafeFlow" Intelligence)
# ---------------------------------------------------------
@router.get("/budget-health/{user_id}")
def check_budget_health(user_id: int, db: Session = Depends(get_conn)):
    """
    Analyzes recent spending habits to provide a 'Nudge'.
    If spending is high this week, it warns the user.
    """
    # specific logic: Get spending for the last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    recent_spending = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, 
                Transaction.transaction_type == 'debit',
                Transaction.timestamp >= seven_days_ago).scalar() or 0.0

    # Determine the status/nudge
    # Note: In a real app, 'budget_limit' would be saved in the database per user.
    # We are using a mock threshold of 50,000 Naira for this demo.
    WEEKLY_LIMIT = 50000.0 
    
    status = "Healthy"
    message = "You are on track! Great job saving this week."
    alert_level = "green"

    if recent_spending > WEEKLY_LIMIT:
        status = "Critical"
        message = f"⚠️ Slow down! You've spent ₦{recent_spending:,.2f} this week, which is above your target."
        alert_level = "red"
    elif recent_spending > (WEEKLY_LIMIT * 0.75):
        status = "Warning"
        message = "You are approaching your weekly spending limit. Try to save for the rest of the week."
        alert_level = "yellow"

    return {
        "period": "Last 7 Days",
        "recent_spending": recent_spending,
        "status": status,
        "alert_level": alert_level,
        "nudge_message": message
    }