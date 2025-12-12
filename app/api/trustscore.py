from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional

from app.db import get_conn
from app.models import User, UserLesson, Transaction

router = APIRouter(prefix="/trustscore", tags=["Trust Score & Credit Identity"])

# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class TrustScoreResponse(BaseModel):
    user_id: int
    score: int
    level: str  # "Newbie", "Bronze", "Silver", "Gold"
    max_loan_eligible: float

class ScoreFactor(BaseModel):
    factor: str
    impact: str # "High", "Medium", "Low"
    description: str

class BreakdownResponse(BaseModel):
    total_score: int
    factors: List[ScoreFactor]

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def calculate_level(score: int):
    if score >= 750: return "Gold", 50000.0
    if score >= 600: return "Silver", 20000.0
    if score >= 450: return "Bronze", 5000.0
    return "Newbie", 0.0

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@router.get("/{user_id}", response_model=TrustScoreResponse)
def get_score_summary(user_id: int, db: Session = Depends(get_conn)):
    """
    Get the user's current TrustScore and Loan Eligibility.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    level_name, loan_amount = calculate_level(user.trust_score)
    
    return {
        "user_id": user.id,
        "score": user.trust_score,
        "level": level_name,
        "max_loan_eligible": loan_amount
    }

@router.get("/{user_id}/breakdown", response_model=BreakdownResponse)
def get_score_breakdown(user_id: int, db: Session = Depends(get_conn)):
    """
    Explains WHY the score is high or low.
    This transparency builds trust with the user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    factors = []

    # Factor 1: Education (Lessons Completed)
    lesson_count = db.query(UserLesson).filter(UserLesson.user_id == user_id).count()
    if lesson_count > 0:
        factors.append({
            "factor": "Financial Literacy",
            "impact": "High",
            "description": f"You have completed {lesson_count} financial lessons. Great job!"
        })
    else:
        factors.append({
            "factor": "Financial Literacy",
            "impact": "Negative",
            "description": "You haven't completed any lessons yet. Start learning to boost your score."
        })

    # Factor 2: Activity (Transaction History)
    tx_count = db.query(Transaction).filter(
        Transaction.user_id == user_id, 
        Transaction.status == "completed"
    ).count()
    
    if tx_count > 5:
        factors.append({
            "factor": "Account Activity",
            "impact": "Medium",
            "description": "You use your wallet frequently and responsibly."
        })
    
    # Factor 3: Account Age / Base
    factors.append({
        "factor": "Base Score",
        "impact": "Low",
        "description": "Standard starting score for verified users."
    })

    return {
        "total_score": user.trust_score,
        "factors": factors
    }