# app/routers/students.py
from typing import Optional
from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import examen
from app.models import student
from app.models.student import Student
from app.models.result import ResultatFinal
from app.models.ec import EC
from app.core.utils import calculate_overall_status
from app.core.security import get_current_student
from app.schemas.result import StudentResultsResponse
from app.models.examen import Examen
from collections import defaultdict



router = APIRouter()

@router.get("/{student_id}/results", response_model=StudentResultsResponse)
async def get_student_results(
    student_id: int,
    examen_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_student_raw: Student = Depends(get_current_student)
):
    # Charger l'étudiant connecté avec sa relation niveau
    current_student = db.query(Student).options(joinedload(Student.niveau)).filter(Student.id == current_student_raw.id).first()

    if current_student.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")

    results = db.query(ResultatFinal).filter(
        ResultatFinal.etudiant_id == student_id
    ).options(
        joinedload(ResultatFinal.ec).joinedload(EC.ue),
        joinedload(ResultatFinal.examen)
    ).all()

    # Grouper par UE
    grouped_results = defaultdict(list)

    for r in results:
        if r.ec and r.ec.ue:
            ue_key = (r.ec.ue.id, r.ec.ue.nom, r.ec.ue.credits)
            grouped_results[ue_key].append({
                "ec_nom": r.ec.nom,
                "note": r.note,
                "decision": r.decision
            })

    ue_results = []
    for (ue_id, ue_nom, ue_credits), ec_list in grouped_results.items():
        ue_results.append({
            "ue_nom": ue_nom,
            "ue_credit": ue_credits,
            "ecs": ec_list
        })

    overall_status = calculate_overall_status(results)
    average = sum([r.note for r in results]) / len(results) if results else None

    return {
        "student": {
            "id": current_student.id,
            "matricule": current_student.matricule,
            "nom": current_student.nom,
            "prenom": current_student.prenom,
            "sexe": current_student.sexe,
            "is_active": current_student.is_active,
            "niveau": f"{current_student.niveau.nom} ({current_student.niveau.abr})" if current_student.niveau else None
        },
        "results": ue_results,
        "overall_status": overall_status,
        "average": average
    }



@router.get("/me")
async def get_current_user_info(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    student = db.query(Student).options(
        joinedload(Student.niveau)
    ).filter(Student.id == current_student.id).first()

    return {
        "id": student.id,
        "matricule": student.matricule,
        "nom": student.nom,
        "prenom": student.prenom,
        "sexe": student.sexe,
        "is_active": student.is_active,
        "niveau": f"{student.niveau.nom} ({student.niveau.abr})" if student.niveau else None
    }

@router.get("/{student_id}/examens")
async def get_available_examens_for_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    if current_student.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")

    examens_ids = db.query(ResultatFinal.examen_id).filter(
        ResultatFinal.etudiant_id == student_id
    ).distinct()

    exams = db.query(Examen).filter(Examen.id.in_(examens_ids)).all()

    return [{"id": e.id, "libelle": f"Session {e.id}"} for e in exams]

