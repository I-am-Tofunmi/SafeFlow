import os
import pickle
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ai", tags=["AI & ScamShield"])

# ---------------------------------------------------------
# 1. Setup & Model Loading
# ---------------------------------------------------------

# Paths to the ML artifacts (created by train_sms_model.py)
MODEL_PATH = "ml/sms_spam_model.pkl"
VECTORIZER_PATH = "ml/vectorizer.pkl"

class SMSAnalysisRequest(BaseModel):
    sender: str
    text: str
    
class SMSAnalysisResponse(BaseModel):
    is_suspicious: bool
    risk_level: str  # "Low", "Medium", "High"
    reason: str
    confidence: float

# Global variables to hold the loaded model
model = None
vectorizer = None

def load_ml_artifacts():
    """
    Attempts to load the trained ML model and vectorizer.
    """
    global model, vectorizer
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                vectorizer = pickle.load(f)
            print("✅ AI: ML Model loaded successfully.")
        else:
            print("⚠️ AI: Model files not found. Using Rule-Based mode only.")
    except Exception as e:
        print(f"❌ AI: Error loading model: {e}")

# Load model when this module is imported (or on startup)
load_ml_artifacts()

# ---------------------------------------------------------
# 2. Rule-Based Logic (The "Safety Net")
# ---------------------------------------------------------
def check_rules(text: str, sender: str):
    """
    Simple keyword analysis for rapid detection without ML.
    Useful for low-end devices or immediate flags.
    """
    text_lower = text.lower()
    triggers = [
        "congratulations", "you have won", "urgent", "account blocked", 
        "click this link", "verify your bvn", "otp", "password"
    ]
    
    # 1. Check for suspicious keywords
    for trigger in triggers:
        if trigger in text_lower:
            return True, "High", f"Contains suspicious keyword: '{trigger}'"
            
    # 2. Check for unexpected shortcodes (Example logic)
    if len(sender) < 6 and not sender.isalpha():
        # Valid banks often use names (e.g., 'GTBank'), unknown short numbers can be risky
        pass 

    return False, "Low", "No immediate keywords detected."

# ---------------------------------------------------------
# 3. The API Endpoint
# ---------------------------------------------------------
@router.post("/analyze-sms", response_model=SMSAnalysisResponse)
def analyze_sms(request: SMSAnalysisRequest):
    """
    Analyzes an incoming SMS to detect scams.
    Uses ML if available, otherwise falls back to rules.
    """
    risk_score = 0.0
    is_suspicious = False
    reason = "Safe"
    risk_level = "Low"

    # Step 1: Run Rule-Based Check (Fastest)
    rule_suspicious, rule_level, rule_reason = check_rules(request.text, request.sender)
    
    if rule_suspicious:
        # If rules catch it, we trust the rules immediately
        return {
            "is_suspicious": True,
            "risk_level": rule_level,
            "reason": rule_reason,
            "confidence": 0.95
        }

    # Step 2: Run ML Model (If loaded)
    if model and vectorizer:
        try:
            # Transform text to numbers
            features = vectorizer.transform([request.text])
            # Predict (1 = Scam, 0 = Ham)
            prediction = model.predict(features)[0]
            # Get probability/confidence
            proba = model.predict_proba(features)[0][1] # Probability of being scam
            
            if prediction == 1:
                is_suspicious = True
                risk_level = "High" if proba > 0.8 else "Medium"
                reason = "AI Pattern Match: Text resembles known scam formats."
                risk_score = proba
            else:
                reason = "AI Analysis passed."
                risk_score = proba
                
        except Exception as e:
            # If ML fails, default to safe but log warning
            print(f"ML Prediction Error: {e}")
            reason = "AI Error - Defaulted to Rules"

    return {
        "is_suspicious": is_suspicious,
        "risk_level": risk_level,
        "reason": reason,
        "confidence": risk_score
    }