from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.db import get_conn
from app.models import Contact, User

router = APIRouter(prefix="/contacts", tags=["Contacts & Beneficiaries"])

# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class ContactCreate(BaseModel):
    name: str
    phone_number: str

class ContactResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    is_trusted: bool
    
    class Config:
        from_attributes = True

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@router.post("/", response_model=ContactResponse)
def add_contact(contact: ContactCreate, user_id: int, db: Session = Depends(get_conn)):
    """
    Save a new beneficiary.
    Validates if the phone number is valid (simple length check).
    """
    # 1. Simple validation
    if len(contact.phone_number) < 10:
        raise HTTPException(status_code=400, detail="Invalid phone number length.")

    # 2. Check if contact already exists for this user
    existing = db.query(Contact).filter(
        Contact.user_id == user_id, 
        Contact.phone_number == contact.phone_number
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Contact already saved.")

    # 3. Create the contact
    # Note: New contacts start as "is_trusted=False" until you send money safely.
    new_contact = Contact(
        user_id=user_id,
        name=contact.name,
        phone_number=contact.phone_number,
        is_trusted=False 
    )
    
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    
    return new_contact

@router.get("/", response_model=List[ContactResponse])
def get_contacts(user_id: int, db: Session = Depends(get_conn)):
    """
    List all saved beneficiaries for a user.
    """
    contacts = db.query(Contact).filter(Contact.user_id == user_id).all()
    return contacts

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_conn)):
    """
    Remove a beneficiary.
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}