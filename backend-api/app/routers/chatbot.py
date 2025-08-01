# app/routers/chatbot.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.schemas.result import StudentResultsResponse
from app.utils.result_formatter import get_results_for_student
from app.schemas.student import StudentProfileResponse
from app.schemas.chatbot import MatriculeRequest
from app.models.user import User
from app.core.security import verify_password
from app.schemas.chatbot import ChatbotLoginRequest

router = APIRouter(prefix="/api/v1/chatbot", tags=["Chatbot"])

@router.post("/check")
def verify_matricule(request: MatriculeRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.matricule == request.matricule).first()
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé.")
    return {
        "id": student.id,
        "nom": student.nom,
        "prenom": student.prenom,
        "matricule": student.matricule,
    }

@router.get("/student/{matricule}")
def verify_student(matricule: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.matricule == matricule).first()
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")
    return {
        "id": student.id,
        "nom": student.nom,
        "prenom": student.prenom,
        "matricule": student.matricule,
    }


@router.get("/student/{student_id}/profile", response_model=StudentProfileResponse)
def get_student_profile(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")

    return {
        "id": student.id,
        "nom": student.nom,
        "prenom": student.prenom,
        "matricule": student.matricule,
        "sexe": "Masculin" if student.sexe == "M" else "Féminin",
        "niveau": f"{student.niveau.nom} ({student.niveau.abr})" if student.niveau else None
    }


@router.get("/student/{student_id}/results", response_model=StudentResultsResponse)
def get_student_results(student_id: int, db: Session = Depends(get_db)):
    return get_results_for_student(student_id, db)


@router.post("/login")
def chatbot_login(data: ChatbotLoginRequest, db: Session = Depends(get_db)):
    # Étape 1 : Vérifier l'étudiant via le matricule
    student = db.query(Student).filter(Student.matricule == data.matricule).first()
    if not student:
        raise HTTPException(status_code=401, detail="Matricule invalide")

    # Étape 2 : Récupérer le compte utilisateur lié
    user = db.query(User).filter(User.etudiant_id == student.id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Aucun compte utilisateur trouvé pour ce matricule.")

    # Étape 3 : Vérifier le mot de passe
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect.")

    # Succès
    return {
        "id": student.id,
        "nom": student.nom,
        "prenom": student.prenom,
        "matricule": student.matricule,
    }
