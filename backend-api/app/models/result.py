# app/models/result.py
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ResultatFinal(Base):
    __tablename__ = "resultats_finaux"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    examen_id = Column(Integer, ForeignKey("examens.id"), nullable=True)
    ec_id = Column(Integer, ForeignKey("ecs.id"), nullable=True)

    note = Column(Float, nullable=True)
    decision = Column(String(255), nullable=True)
    statut = Column(String(50), nullable=True)
    jury_validated = Column(Boolean, default=False)

    # Relations
    etudiant = relationship("Student", back_populates="resultats")
    examen = relationship("Examen", back_populates="resultats")
    ec = relationship("EC")  # EC.ue est accessible grâce à cette relation
