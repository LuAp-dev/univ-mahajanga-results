from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class EC(Base):
    __tablename__ = "ecs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    abr = Column(String(50)) 
    coefficient = Column(Float, default=1.0) 

    resultats = relationship("ResultatFinal", back_populates="ec")

