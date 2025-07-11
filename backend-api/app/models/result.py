# app/models/result.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base




class ResultatFinal(Base):
    __tablename__ = "resultats_finaux"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("etudiants.id"))
    examen_id = Column(Integer, ForeignKey("examens.id"))
    ec_id = Column(Integer, ForeignKey("ecs.id"))  
    note = Column(Float)
    decision = Column(String)  
    statut = Column(String)    
    jury_validated = Column(Boolean)  

    etudiant = relationship("Student", back_populates="resultats")
    examen = relationship("Examen", back_populates="resultats")
    ec = relationship("EC") 

    etudiant = relationship("Student", back_populates="resultats")
    examen = relationship("Examen", back_populates="resultats")

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
    resultats = relationship("ResultatFinal", back_populates="examen")