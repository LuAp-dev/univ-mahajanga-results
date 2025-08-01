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
from app.models.user import User
from app.core.security import verify_password


SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Étape 1 : Vérifie que le matricule correspond à un étudiant
    student = db.query(Student).filter(Student.matricule == data.matricule).first()
    if not student:
        raise HTTPException(status_code=401, detail="Matricule invalide")

    # Étape 2 : Vérifie qu'un utilisateur est lié à cet étudiant
    user = db.query(User).filter(User.etudiant_id == student.id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Aucun compte utilisateur associé à ce matricule.")

    # Étape 3 : Vérifie que le mot de passe est correct
    if not verify_password(data.password, user.password):  # ici, .password = champ réel en BDD
        raise HTTPException(status_code=401, detail="Mot de passe invalide")

    # Étape 4 : Génère le token JWT
    jwt_token = create_access_token(data={"sub": str(student.id)})

    # Étape 5 : Renvoie la réponse
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

