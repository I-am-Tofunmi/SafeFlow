from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

# ---------------------------------------------------------
# 1. User Model (Auth & Identity)
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    
    # Financial Identity
    trust_score = Column(Integer, default=300) # Starts at 300
    is_active = Column(Boolean, default=True)
    
    # Relationships (Links to other tables)
    transactions = relationship("Transaction", back_populates="owner")
    contacts = relationship("Contact", back_populates="owner")
    lessons_completed = relationship("UserLesson", back_populates="user")

# ---------------------------------------------------------
# 2. Transaction Model (Money Movement)
# ---------------------------------------------------------
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    amount = Column(Float)
    transaction_type = Column(String)  # 'credit' or 'debit'
    status = Column(String)            # 'pending', 'completed', 'flagged'
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    owner = relationship("User", back_populates="transactions")

# ---------------------------------------------------------
# 3. Contact Model (Beneficiaries)
# ---------------------------------------------------------
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    name = Column(String)
    phone_number = Column(String)
    is_trusted = Column(Boolean, default=False)  # True if you've sent money safely before
    
    # Relationship
    owner = relationship("User", back_populates="contacts")

# ---------------------------------------------------------
# 4. Lesson Model (Financial Education Content)
# ---------------------------------------------------------
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    language = Column(String) # 'english', 'pidgin', 'yoruba', 'hausa'
    category = Column(String) # 'security', 'savings', 'credit'
    xp_points = Column(Integer, default=10)

# ---------------------------------------------------------
# 5. UserLesson Model (Tracking Progress)
# ---------------------------------------------------------
class UserLesson(Base):
    __tablename__ = "user_lessons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="lessons_completed")