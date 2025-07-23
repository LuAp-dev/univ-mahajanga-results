# app/models/ec.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.ue import UE

class EC(Base):
    __tablename__ = "ecs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    abr = Column(String(10), nullable=False)
    coefficient = Column(Float, nullable=False)
    ue_id = Column(Integer, ForeignKey("ues.id"))

    # Relation vers l'UE
    ue = relationship(UE, back_populates="ecs")
