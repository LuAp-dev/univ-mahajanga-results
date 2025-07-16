from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.result import ResultatFinal
from app.schemas.result import StudentResultsResponse
from app.core.utils import calculate_overall_status
from app.core.security import get_current_student


router = APIRouter()

@router.get("/{student_id}/results", response_model=StudentResultsResponse)
async def get_student_results(
    student_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    if current_student.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")

    results = db.query(ResultatFinal).filter(
        ResultatFinal.etudiant_id == student_id
    ).options(
        joinedload(ResultatFinal.ec),
        joinedload(ResultatFinal.examen)
    ).all()

    results_response = [{
        "id": r.id,
        "note": r.note,
        "decision": r.decision,
        "statut": r.statut,
        "jury_validated": r.jury_validated,
        "ec_nom": r.ec.nom if r.ec else None,
        "ec_nom": r.ec.nom if r.ec else None,
        "ec_code": r.ec.abr if r.ec else None,
        "examen_nom": f"Session {r.examen.id}" if r.examen else None
} for r in results]

    overall_status = calculate_overall_status(results)
    average = sum([r.note for r in results]) / len(results) if results else None

    return {
        "student": {
            "id": current_student.id,
            "matricule": current_student.matricule,
            "nom": current_student.nom,
            "prenom": current_student.prenom,
            "sexe": current_student.sexe,
            "is_active": current_student.is_active
        },
        "results": results_response,
        "overall_status": overall_status,
        "average": average
    }

