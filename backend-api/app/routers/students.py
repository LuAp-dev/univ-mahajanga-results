# app/routers/students.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.result import ResultatFinal
from app.schemas.result import StudentResultsResponse
from app.core.security import get_current_student

router = APIRouter()

@router.get("/{student_id}/results", response_model=StudentResultsResponse)
async def get_student_results(
    student_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # Vérifier que l'étudiant peut accéder à ses propres résultats
    if current_student.id != student_id:
        raise HTTPException(
            status_code=403,
            detail="Accès non autorisé"
        )
    
    # Récupérer les résultats
    results = db.query(ResultatFinal).filter(
        ResultatFinal.etudiant_id == student_id
    ).all()
    
    # Calculer le statut global
    overall_status = calculate_overall_status(results)
    
    return {
        "student": current_student,
        "results": results,
        "overall_status": overall_status
    }

def calculate_overall_status(results):
    """Calculer le statut global de l'étudiant"""
    if not results:
        return "AUCUN_RESULTAT"
    
    decisions = [r.decision for r in results]
    
    if "exclus" in decisions:
        return "EXCLUS"
    elif "redoublant" in decisions:
        return "REDOUBLANT"
    elif "rattrapage" in decisions:
        return "RATTRAPAGE"
    else:
        return "ADMIS"