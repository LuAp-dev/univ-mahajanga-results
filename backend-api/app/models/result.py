from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ResultatFinal(Base):
    __tablename__ = "resultats_finaux"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"))
    examen_id = Column(Integer, ForeignKey("examens.id"))
    ec_id = Column(Integer, ForeignKey("ecs.id"))  
    
    note = Column(Float)
    decision = Column(String)  
    statut = Column(String)    
    jury_validated = Column(Boolean)  

    etudiant = relationship("Student", back_populates="resultats")
    examen = relationship("Examen", back_populates="resultats")
    ec = relationship("EC", back_populates="resultats")
