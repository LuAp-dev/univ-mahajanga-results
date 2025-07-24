# app/models/niveau.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Niveau(Base):
    __tablename__ = "niveaux"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    abr = Column(String(20))
    etudiants = relationship("Student", back_populates="niveau")

