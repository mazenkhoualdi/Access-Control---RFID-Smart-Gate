from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class Equipe(Base):
    __tablename__ = "Equipe"
    
    id_equipe = Column(Integer, primary_key=True)
    nom_equipe = Column(String(50), nullable=False, unique=True)

    employes = relationship("Employe", back_populates="equipe")

Base.metadata.create_all(engine)
