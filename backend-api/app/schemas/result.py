# app/schemas/result.py


##


from pydantic import BaseModel
from typing import Optional, ForwardRef
from .student import StudentBase  # Importez seulement ce dont vous avez besoin

# Solution pour la dépendance circulaire
StudentResponse = ForwardRef('StudentResponse')

class StudentResultsResponse(BaseModel):
    student: StudentResponse
    average: Optional[float] = None

# Import différé pour résoudre la référence circulaire
from .student import StudentResponse
StudentResultsResponse.update_forward_refs()


##


from pydantic import BaseModel
from typing import List, Optional

class ResultBase(BaseModel):
    note: float
    decision: str
    statut: str

class ResultResponse(ResultBase):
    id: int
    ec_nom: str
    ec_code: str
    examen_nom: str
    jury_validated: bool
    
    class Config:
        from_attributes = True

class StudentResultsResponse(BaseModel):
    student: StudentResponse
    results: List[ResultResponse]
    overall_status: str
    average: Optional[float] = None