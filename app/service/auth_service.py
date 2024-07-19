from app.schema.user_schema import UserCreate, UserLogin, Token
from app.model.user import User
from app.repository.user_repository import UserRepository
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = "SECRET_KEY"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def signup(self, user: UserCreate) -> Token:
        user.password = self.hash_password(user.password)
        db_user = self.user_repository.create_user(user)
        return self.create_token(db_user)

    def login(self, user: UserLogin) -> Token:
        db_user = self.user_repository.get_user_by_email(user.email)
        if not db_user or not self.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return self.create_token(db_user)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_token(self, user: User) -> Token:
        to_encode = {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return {"access_token": encoded_jwt, "token_type": "bearer"}
