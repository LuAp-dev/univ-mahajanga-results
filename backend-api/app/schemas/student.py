# app/schemas/student.py
from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    sexe: Optional[str]

class StudentResponse(StudentBase):
    id: int
    matricule: str
    niveau: Optional[str]

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    matricule: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    student: StudentResponse