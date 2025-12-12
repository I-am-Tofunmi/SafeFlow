from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db import get_conn
from app.models import Lesson, UserLesson, User

router = APIRouter(prefix="/lessons", tags=["Education & Literacy"])

# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    language: str
    category: str
    xp_points: int

    class Config:
        from_attributes = True

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@router.get("/", response_model=List[LessonResponse])
def get_lessons(language: Optional[str] = "english", db: Session = Depends(get_conn)):
    """
    Get all available lessons, filtered by language.
    """
    lessons = db.query(Lesson).filter(Lesson.language == language).all()
    return lessons

@router.post("/{lesson_id}/complete")
def complete_lesson(lesson_id: int, user_id: int, db: Session = Depends(get_conn)):
    """
    Mark a lesson as complete and BOOST the user's TrustScore.
    """
    # 1. Check if lesson exists
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # 2. Check if already completed
    existing_completion = db.query(UserLesson).filter(
        UserLesson.user_id == user_id,
        UserLesson.lesson_id == lesson_id
    ).first()

    if existing_completion:
        return {"message": "Lesson already completed", "new_score": None}

    # 3. Record completion
    user_lesson = UserLesson(user_id=user_id, lesson_id=lesson_id)
    db.add(user_lesson)

    # 4. UPDATE TRUST SCORE
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.trust_score += lesson.xp_points
    
    db.commit()

    return {
        "message": "Lesson completed!", 
        "points_earned": lesson.xp_points,
        "new_trust_score": user.trust_score
    }

# ---------------------------------------------------------
# Helper: Seed Data
# ---------------------------------------------------------
@router.post("/seed")
def seed_lessons(db: Session = Depends(get_conn)):
    """
    Populates the DB with initial lessons.
    """
    if db.query(Lesson).count() > 0:
        return {"message": "Lessons already exist."}

    sample_lessons = [
        Lesson(
            title="Spotting Fake Alerts",
            content="Always check your actual bank app balance. SMS alerts can be faked.",
            language="english",
            category="security",
            xp_points=15
        ),
        Lesson(
            title="Why Save Small Small?",
            content="Saving 100 Naira daily adds up to 36,500 Naira a year.",
            language="english",
            category="savings",
            xp_points=10
        ),
        Lesson(
            title="No fall maga!",
            content="If person call you say make you send OTP, abeg cut call immediately.",
            language="pidgin",
            category="security",
            xp_points=15
        ),
        Lesson(
            title="Credit Score na your reputation",
            content="When you borrow, pay back quick. E go make banks trust you.",
            language="pidgin",
            category="credit",
            xp_points=20
        )
    ]

    db.add_all(sample_lessons)
    db.commit()
    return {"message": "Sample lessons created successfully!"}