# app/models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id", ondelete="CASCADE"), nullable=False)
    password = Column(String, nullable=False)

    etudiant = relationship("Student", back_populates="user")
