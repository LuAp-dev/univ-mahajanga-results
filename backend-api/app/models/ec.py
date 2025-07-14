from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class EC(Base):
    __tablename__ = "ecs"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    code = Column(String(50))
    credit = Column(Integer)

    resultats = relationship("ResultatFinal", back_populates="ec")
