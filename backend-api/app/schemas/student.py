# app/schemas/student.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudentBase(BaseModel):
    matricule: str
    nom: str
    prenom: str
    sexe: str

class StudentResponse(StudentBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    matricule: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    student: StudentResponse