# app/models/ue.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class UE(Base):
    __tablename__ = "ues"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    credits = Column(Float, nullable=True)

    # Relation vers les ECs
    ecs = relationship("EC", back_populates="ue")
