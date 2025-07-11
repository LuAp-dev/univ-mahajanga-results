class ElementConstitutif(Base):
    __tablename__ = "elements_constitutifs"
    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    code = Column(String(50))
    
    resultats = relationship("ResultatFinal", back_populates="ec")

