from sqlalchemy.orm import Session
from db import get_db, User
from models.event import UserInterests

def add_test_user():
    db: Session = next(get_db())
    interests = UserInterests(
        categories=[1, 2],
        preferences={"max_radius": 10, "min_overlap_hours": 2}
    )
    user = User(id=1, email="test@example.com", interests=interests.dict())
    db.add(user)
    db.commit()
    db.close()

if __name__ == "__main__":
    add_test_user()