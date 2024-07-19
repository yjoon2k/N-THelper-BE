from fastapi import APIRouter, Depends, HTTPException, status
from app.schema.user_schema import UserCreate, UserLogin, Token
from app.service.auth_service import AuthService
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.signup(user)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.login(user)
