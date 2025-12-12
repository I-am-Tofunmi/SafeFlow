from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db import get_conn
from app.models import User
from app.utils import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ---------------------------------------------------------
# Pydantic Models (Validation)
# ---------------------------------------------------------
class UserSignup(BaseModel):
    phone_number: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    phone_number: str
    password: str

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup, db: Session = Depends(get_conn)):
    """
    Register a new user using Phone Number.
    """
    # 1. Check if user already exists
    existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    # 2. Hash the password (Security First)
    hashed_pw = get_password_hash(user.password)

    # 3. Create new user instance
    # We set a default trust_score of 300 (Starter score for credit invisibility)
    new_user = User(
        phone_number=user.phone_number,
        full_name=user.full_name,
        hashed_password=hashed_pw,
        trust_score=300,
        is_active=True
    )

    # 4. Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup Successful", "user_id": new_user.id}

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_conn)):
    """
    Login with Phone Number and Password.
    """
    # 1. Find user by phone
    user = db.query(User).filter(User.phone_number == user_credentials.phone_number).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 2. Verify password
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3. Check if account is active (Safety feature)
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Please contact support."
        )

    # In a real production app, you would generate a JWT token here.
    # For the hackathon/demo, returning the user_id is sufficient.
    return {
        "message": "Login successful",
        "user_id": user.id,
        "full_name": user.full_name,
        "current_trust_score": user.trust_score,
        "token": "demo-token-12345" 
    }