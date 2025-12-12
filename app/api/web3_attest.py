import hashlib
import json
import secrets
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_conn
from app.models import User

router = APIRouter(prefix="/web3", tags=["Web3 Identity & Attestation"])

# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class AttestationRequest(BaseModel):
    wallet_address: str  # The user's crypto wallet (e.g., 0x123...)

class AttestationResponse(BaseModel):
    user_id: int
    trust_score: int
    attestation_hash: str
    transaction_hash: str
    block_number: int
    status: str
    explorer_link: str

# ---------------------------------------------------------
# Helper: Simulate Blockchain Hashing
# ---------------------------------------------------------
def generate_mock_tx_hash(data: str):
    """
    Creates a fake but realistic-looking Ethereum transaction hash.
    """
    raw_string = f"{data}{secrets.token_hex(8)}{datetime.utcnow()}"
    return "0x" + hashlib.sha256(raw_string.encode()).hexdigest()

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@router.post("/mint-identity/{user_id}", response_model=AttestationResponse)
def mint_identity_token(user_id: int, request: AttestationRequest, db: Session = Depends(get_conn)):
    """
    Mints a 'Reputation Token' (SBT - Soulbound Token) representing the user's score.
    
    In a real production app, this would use `web3.py` to call a Smart Contract.
    Here, we simulate the success for the demo.
    """
    # 1. Get User Data
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.trust_score < 400:
        raise HTTPException(status_code=400, detail="TrustScore too low to mint identity. Minimum 400 required.")

    # 2. Create the Data Payload (The 'Attestation')
    attestation_data = {
        "user_id": user.id,
        "score": user.trust_score,
        "timestamp": str(datetime.utcnow()),
        "issuer": "SafeFlow_DAO"
    }
    data_string = json.dumps(attestation_data, sort_keys=True)
    
    # 3. Simulate Blockchain Interaction
    # Generate a hash of the data (Proof of Score)
    attestation_hash = hashlib.sha256(data_string.encode()).hexdigest()
    
    # Generate a fake Transaction Hash (What you see on Etherscan)
    tx_hash = generate_mock_tx_hash(data_string)
    
    # Simulate a block number
    block_num = 18492000 + secrets.randbelow(1000)

    return {
        "user_id": user.id,
        "trust_score": user.trust_score,
        "attestation_hash": attestation_hash,
        "transaction_hash": tx_hash,
        "block_number": block_num,
        "status": "Minted on-chain",
        "explorer_link": f"https://mumbai.polygonscan.com/tx/{tx_hash}"
    }