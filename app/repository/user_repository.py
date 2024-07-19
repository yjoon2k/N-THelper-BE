from sqlalchemy.orm import Session
from app.model.user import User
from app.schema.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        db_user = User(email=user.email, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
