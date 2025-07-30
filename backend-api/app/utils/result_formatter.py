#app/utils/result_formatter.py
from sqlalchemy.orm import Session
from app.models.result import ResultatFinal
from app.models.student import Student
from app.schemas.result import StudentResultsResponse, StudentInfo, UEResult, ECResult

def get_results_for_student(student_id: int, db: Session) -> StudentResultsResponse:
    # Étudiant
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError("Étudiant introuvable")

    # Résultats
    raw_results = (
        db.query(ResultatFinal)
        .filter(ResultatFinal.etudiant_id == student_id)
        .all()
    )

    ue_dict = {}
    total_notes = 0
    total_count = 0

    for res in raw_results:
        ec = res.ec
        ue = ec.ue
        if ue.nom not in ue_dict:
            ue_dict[ue.nom] = {
                "ue_nom": ue.nom,
                "ue_credit": ue.credits or 0,
                "ecs": [],
            }
        ue_dict[ue.nom]["ecs"].append(
            ECResult(ec_nom=ec.nom, note=res.note, decision=res.decision)
        )

        # Moyenne
        if res.note is not None:
            total_notes += res.note
            total_count += 1

    result_data = [
        UEResult(ue_nom=ue["ue_nom"], ue_credit=ue["ue_credit"], ecs=ue["ecs"])
        for ue in ue_dict.values()
    ]

    average = round(total_notes / total_count, 2) if total_count > 0 else None
    overall_status = (
        "Admis" if average is not None and average >= 10
        else "Ajourné" if average is not None
        else "Inconnu"
    )

    return StudentResultsResponse(
        student=StudentInfo(
            id=student.id,
            nom=student.nom,
            prenom=student.prenom,
            matricule=student.matricule,
            sexe=student.sexe,
            is_active=student.is_active,
        ),
        results=result_data,
        average=average,
        overall_status=overall_status,
    )


