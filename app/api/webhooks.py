from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_conn
from app.models import Transaction, User

router = APIRouter(prefix="/webhooks", tags=["External Integrations"])

# ---------------------------------------------------------
# Paystack / Flutterwave Simulation
# ---------------------------------------------------------

@router.post("/payment-notification")
async def receive_payment_webhook(request: Request, db: Session = Depends(get_conn)):
    """
    Receives real-time payment updates from an external provider (e.g., Paystack).
    
    Example Payload:
    {
        "event": "charge.success",
        "data": {
            "reference": "ref_12345",
            "amount": 5000,
            "status": "success",
            "customer_phone": "08012345678"
        }
    }
    """
    try:
        # 1. Parse incoming data
        payload = await request.json()
        event_type = payload.get("event")
        data = payload.get("data", {})
        
        print(f"🔔 Webhook Received: {event_type}")

        # 2. Security Check (Mock)
        # In a real app, you verify the 'x-paystack-signature' header here.
        # if not verify_signature(request.headers): raise HTTPException...

        # 3. Handle Successful Payments
        if event_type == "charge.success":
            phone = data.get("customer_phone")
            amount = data.get("amount")
            
            # Find the user
            user = db.query(User).filter(User.phone_number == phone).first()
            if user:
                # Create a credit transaction automatically
                new_tx = Transaction(
                    user_id=user.id,
                    amount=amount,
                    transaction_type="credit",
                    status="completed"
                )
                db.add(new_tx)
                
                # Bonus: Boost TrustScore for verifying an external funding source
                if user.trust_score < 500:
                    user.trust_score += 5
                    
                db.commit()
                return {"status": "Transaction recorded", "new_balance_update": "queued"}
            
            else:
                print(f"⚠️ Webhook Error: User {phone} not found.")

        return {"status": "Event received"}

    except Exception as e:
        print(f"❌ Webhook Error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid Webhook Data")