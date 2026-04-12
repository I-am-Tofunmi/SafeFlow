from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.db import get_conn
from app.models import Transaction, User, Contact

router = APIRouter(prefix="/transactions", tags=["Transactions & SafeTransfer"])

# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class TransferRequest(BaseModel):
    amount: float
    receiver_phone: str
    description: Optional[str] = "Transfer"

class DepositRequest(BaseModel):
    amount: float

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    status: str
    timestamp: datetime
    message: str

# ---------------------------------------------------------
# Helper: Get Current Balance
# ---------------------------------------------------------
def get_wallet_balance(user_id: int, db: Session):
    """
    Calculates the live balance dynamically.
    """
    credits = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, 
                Transaction.transaction_type == 'credit',
                Transaction.status == 'completed').scalar() or 0.0
                
    debits = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, 
                Transaction.transaction_type == 'debit',
                Transaction.status == 'completed').scalar() or 0.0
                
    return credits - debits

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@router.post("/deposit")
def deposit_money(request: DepositRequest, user_id: int, db: Session = Depends(get_conn)):
    """
    Simulate funding the wallet (e.g., from a real bank).
    Always succeeds for demo purposes.
    """
    tx = Transaction(
        user_id=user_id,
        amount=request.amount,
        transaction_type="credit",
        status="completed"
    )
    db.add(tx)
    db.commit()
    return {"message": f"Successfully deposited ₦{request.amount:,.2f}", "new_balance": get_wallet_balance(user_id, db)}


@router.post("/transfer", response_model=TransactionResponse)
def send_money(request: TransferRequest, user_id: int, db: Session = Depends(get_conn)):
    """
    The Main Transfer Logic with SAFEFLOW GUARD.
    """
    # 1. Check Balance
    current_balance = get_wallet_balance(user_id, db)
    if current_balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    # 2. Analyze Risk (SafeTransfer Logic)
    tx_status = "completed"
    risk_message = "Transfer successful."
    
    # Check if beneficiary is a saved contact
    known_contact = db.query(Contact).filter(
        Contact.user_id == user_id, 
        Contact.phone_number == request.receiver_phone
    ).first()

    # RISK RULE 1: Unknown Number + Large Amount
    # If sending > 10,000 to a stranger, FLAG IT.
    if not known_contact and request.amount > 10000:
        tx_status = "flagged"
        risk_message = "⚠️ Transfer flagged for security review. Sending large amounts to unknown numbers is risky."
    
    # RISK RULE 2: Suspicious Keywords in description
    suspicious_words = ["prize", "lottery", "investment", "double"]
    if any(word in request.description.lower() for word in suspicious_words):
        tx_status = "flagged"
        risk_message = "⚠️ Transfer flagged. The description contains words often used in scams."

    # 3. Process Transaction
    new_tx = Transaction(
        user_id=user_id,
        amount=request.amount,
        transaction_type="debit",
        status=tx_status
    )
    
    db.add(new_tx)
    
    # 4. If successful, update TrustScore (Gamification)
    if tx_status == "completed":
        # Small reward for legitimate activity
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.trust_score < 800:
            user.trust_score += 1 # Tiny increment for activity
            
    db.commit()
    db.refresh(new_tx)

    return {
        "id": new_tx.id,
        "amount": new_tx.amount,
        "type": "debit",
        "status": tx_status,
        "timestamp": new_tx.timestamp,
        "message": risk_message
    }

@router.get("/history")
def transaction_history(user_id: int, db: Session = Depends(get_conn)):
    """
    View all past transactions.
    """
    txs = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.timestamp.desc()).all()
    return txs

@router.get("/balance")
def get_balance(user_id: int, db: Session = Depends(get_conn)):
    """
    Get Current Balance
    """
    balance = get_wallet_balance(user_id, db)
    return {"balance": balance}