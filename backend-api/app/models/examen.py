from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Examen(Base):
    __tablename__ = "examens"
    id = Column(Integer, primary_key=True, index=True)
    niveau_id = Column(Integer, ForeignKey("niveaux.id"))
    parcours_id = Column(Integer, ForeignKey("parcours.id"), nullable=True)
    duree = Column(Integer)
    note_eliminatoire = Column(Float, nullable=True)
    type = Column(String(255))

    # Relation vers ResultatFinal
    resultats = relationship("ResultatFinal", back_populates="examen")
