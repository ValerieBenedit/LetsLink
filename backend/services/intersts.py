from sqlalchemy.orm import Session
from backend.db import User
from models.event import UserInterests

def get_user_interests(db: Session, user_id: int) -> UserInterests:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.interests:
        raise ValueError("User or interests not found")
    return UserInterests(**user.interests)

def update_user_interests(db: Session, user_id: int, interests: UserInterests):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.interests = interests.dict()
    else:
        user = User(id=user_id, email=f"user{user_id}@example.com", interests=interests.dict())
        db.add(user)
    db.commit()