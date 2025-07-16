# app/schemas/result.py

from typing import List, Optional
from pydantic import BaseModel
from typing import List, Optional

class Result(BaseModel):
    id: int
    note: float
    decision: str
    statut: str
    jury_validated: bool
    # ec_nom: Optional[str]
    ec_code: Optional[str]
    examen_nom: Optional[str] = None

    class Config:
        orm_mode = True

class StudentInfo(BaseModel):
    id: int
    matricule: str
    nom: str
    prenom: str
    sexe: str
    is_active: bool

    class Config:
        orm_mode = True

class StudentResultsResponse(BaseModel):
    student: StudentInfo
    results: List[Result]
    overall_status: str
    average: Optional[float] = None
