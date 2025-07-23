# app/schemas/result.py

from typing import List, Optional
from pydantic import BaseModel
from typing import List, Optional

class ECResult(BaseModel):
    ec_nom: str
    note: float
    decision: Optional[str]

class UEResult(BaseModel):
    ue_nom: str
    ue_credit: float
    ecs: List[ECResult]

class StudentInfo(BaseModel):
    id: int
    nom: str
    prenom: str
    matricule: str
    sexe: Optional[str]
    is_active: bool

class StudentResultsResponse(BaseModel):
    student: StudentInfo
    results: List[UEResult]
    overall_status: Optional[str]
    average: Optional[float]