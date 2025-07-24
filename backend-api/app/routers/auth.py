# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student import LoginRequest, LoginResponse
from app.models.student import Student
from app.core.security import create_access_token
from app.core.config import settings
from app.core.security import create_access_token

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.matricule == data.matricule).first()

    if not student:
        raise HTTPException(status_code=401, detail="Matricule invalide")

    jwt_token = create_access_token(data={"sub": str(student.id)})

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "student": {
            "id": student.id,
            "matricule": student.matricule,
            "nom": student.nom,
            "prenom": student.prenom,
            "sexe": student.sexe,
            "niveau": f"{student.niveau.nom} ({student.niveau.abr})" if student.niveau else None
        }
    }