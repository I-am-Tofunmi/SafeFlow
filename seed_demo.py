from app.db import SessionLocal, engine, Base
from app.models import User, Transaction, Contact, Lesson, UserLesson
from app.utils import get_password_hash
from datetime import datetime, timedelta
import random

# 1. Initialize Database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

def seed_data():
    print("🌱 Seeding SafeFlow Database...")

    # --- CLEANUP (Optional: Remove old data) ---
    # db.query(Transaction).delete()
    # db.query(Contact).delete()
    # db.query(User).delete()
    # db.commit()

    # --- 1. Create Users ---
    # Demo User (The one you will login with)
    demo_password = get_password_hash("password123")
    
    user1 = User(
        phone_number="08012345678", 
        full_name="Emeka Johnson", 
        hashed_password=demo_password, 
        trust_score=350,
        is_active=True
    )
    
    # Another User (To simulate transfers)
    user2 = User(
        phone_number="09099887766", 
        full_name="Fatima Bello", 
        hashed_password=demo_password, 
        trust_score=600,
        is_active=True
    )

    db.add(user1)
    db.add(user2)
    db.commit()
    
    # Refresh to get IDs
    db.refresh(user1)
    db.refresh(user2)

    print(f"✅ Created Users: {user1.full_name} & {user2.full_name}")

    # --- 2. Create Contacts (Beneficiaries) ---
    contact1 = Contact(user_id=user1.id, name="Mama", phone_number="07011122233", is_trusted=True)
    contact2 = Contact(user_id=user1.id, name="My Mechanic", phone_number="08155566677", is_trusted=False)
    
    db.add(contact1)
    db.add(contact2)
    db.commit()
    print("✅ Created Contacts")

    # --- 3. Create Transactions (History) ---
    # Create some random past transactions for the dashboard chart
    transactions = []
    
    # Salary / Income
    transactions.append(Transaction(
        user_id=user1.id, amount=50000, transaction_type="credit", status="completed",
        timestamp=datetime.utcnow() - timedelta(days=10)
    ))
    
    # Food expense
    transactions.append(Transaction(
        user_id=user1.id, amount=2500, transaction_type="debit", status="completed",
        timestamp=datetime.utcnow() - timedelta(days=5)
    ))
    
    # Airtime
    transactions.append(Transaction(
        user_id=user1.id, amount=1000, transaction_type="debit", status="completed",
        timestamp=datetime.utcnow() - timedelta(days=2)
    ))

    # A "Flagged" Attempt (Scam prevented)
    transactions.append(Transaction(
        user_id=user1.id, amount=15000, transaction_type="debit", status="flagged",
        timestamp=datetime.utcnow() - timedelta(hours=1)
    ))

    db.add_all(transactions)
    db.commit()
    print("✅ Created Transaction History")

    print("🚀 Database Seeded Successfully!")

if __name__ == "__main__":
    seed_data()