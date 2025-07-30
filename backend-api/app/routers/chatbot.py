# app/routers/chatbot.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.schemas.result import StudentResultsResponse
from app.utils.result_formatter import get_results_for_student

router = APIRouter(prefix="/api/v1/chatbot", tags=["Chatbot"])

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

@router.get("/student/{student_id}/results", response_model=StudentResultsResponse)
def get_student_results(student_id: int, db: Session = Depends(get_db)):
    return get_results_for_student(student_id, db)


