# app/models/result.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ResultatFinal(Base):
    __tablename__ = "resultats_finaux"
    
    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"))
    examen_id = Column(Integer, ForeignKey("examens.id"))
    ec_id = Column(Integer, ForeignKey("ecs.id"))
    note = Column(Float)
    decision = Column(String(20))
    statut = Column(String(20))
    jury_validated = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relations
    etudiant = relationship("Student", back_populates="resultats")
    ec = relationship("EC")
    examen = relationship("Examen")

class EC(Base):
    __tablename__ = "ecs"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    code = Column(String(50))
    credit = Column(Integer)
    
class Examen(Base):
    __tablename__ = "examens"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    session_id = Column(Integer)
    date_examen = Column(DateTime)