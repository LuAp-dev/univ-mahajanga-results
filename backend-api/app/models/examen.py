from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Examen(Base):
    __tablename__ = "examens"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))

    # Relation vers ResultatFinal
    resultats = relationship("ResultatFinal", back_populates="examen")
