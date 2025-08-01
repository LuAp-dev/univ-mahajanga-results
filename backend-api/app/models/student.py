#app/models/student.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "etudiants"
    
    id = Column(Integer, primary_key=True, index=True)
    matricule = Column(String(50), unique=True, index=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    sexe = Column(String(1))
    niveau_id = Column(Integer, ForeignKey("niveaux.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relations
    resultats = relationship("ResultatFinal", back_populates="etudiant")
    niveau = relationship("Niveau", back_populates="etudiants")
    user = relationship("User", back_populates="etudiant", uselist=False)

from app.models.niveau import Niveau
