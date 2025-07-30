from sqlalchemy.orm import Session
from app.models.result import ResultatFinal
from app.schemas.result import StudentResultsResponse, StudentInfo, UEResult, ECResult

def get_results_for_student(student_id: int, db: Session) -> StudentResultsResponse:
    student = db.query(ResultatFinal.etudiant).filter(ResultatFinal.etudiant_id == student_id).first()
    if not student:
        raise ValueError("Étudiant introuvable")
    
    raw_results = (
        db.query(ResultatFinal)
        .filter(ResultatFinal.etudiant_id == student_id)
        .all()
    )

    ue_dict = {}
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

    result_data = [
        UEResult(ue_nom=ue["ue_nom"], ue_credit=ue["ue_credit"], ecs=ue["ecs"])
        for ue in ue_dict.values()
    ]

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
        average=None,
        overall_status=None,
    )
