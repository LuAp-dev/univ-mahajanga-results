class Examen(Base):
    __tablename__ = "examens"
    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    
    resultats = relationship("ResultatFinal", back_populates="examen")

