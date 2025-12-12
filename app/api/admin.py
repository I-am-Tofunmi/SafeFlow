from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_conn
from app.models import User, Transaction

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

# ---------------------------------------------------------
# 1. System Stats (For the Admin Dashboard Homepage)
# ---------------------------------------------------------
@router.get("/stats")
def get_system_stats(db: Session = Depends(get_conn)):
    """
    Returns high-level metrics for the admin dashboard.
    """
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # Count flagged transactions (Potential scams stopped)
    flagged_tx_count = db.query(Transaction).filter(Transaction.status == "flagged").count()
    
    # Calculate average TrustScore across the platform
    avg_trust_score = db.query(func.avg(User.trust_score)).scalar() or 0

    return {
        "total_users": total_users,
        "active_users": active_users,
        "flagged_transactions": flagged_tx_count,
        "average_trust_score": round(avg_trust_score, 2)
    }

# ---------------------------------------------------------
# 2. User Management
# ---------------------------------------------------------
@router.get("/users")
def list_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_conn)):
    """
    List all users with pagination.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_conn)):
    """
    Ban a user who is violating SafeFlow rules.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    return {"message": f"User {user.full_name} has been deactivated."}

# ---------------------------------------------------------
# 3. Transaction Oversight (SafeTransfer Guard)
# ---------------------------------------------------------
@router.get("/flagged-transactions")
def get_flagged_transactions(db: Session = Depends(get_conn)):
    """
    Retrieve all transactions marked as 'flagged' (potential scams/mistakes)
    so an admin can review them.
    """
    risky_tx = db.query(Transaction).filter(Transaction.status == "flagged").all()
    return risky_tx

@router.post("/resolve-transaction/{tx_id}")
def resolve_transaction(tx_id: int, decision: str, db: Session = Depends(get_conn)):
    """
    Admin decision on a flagged transaction.
    decision can be 'approve' (allow it) or 'reject' (block it).
    """
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if decision == "approve":
        tx.status = "completed"
        msg = "Transaction approved and processed."
    elif decision == "reject":
        tx.status = "rejected"
        msg = "Transaction blocked for safety."
    else:
        raise HTTPException(status_code=400, detail="Invalid decision. Use 'approve' or 'reject'.")

    db.commit()
    return {"message": msg, "transaction_id": tx.id, "new_status": tx.status}