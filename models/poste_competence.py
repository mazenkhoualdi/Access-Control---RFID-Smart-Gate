from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class PosteCompetence(Base):
    __tablename__ = "Poste_Competence"
    id_poste = Column(Integer, primary_key=True)
    nom_poste = Column(String(50), nullable=False)
    competence = Column(String(50), nullable=False)
    etoiles = Column(Integer, nullable=False)

Base.metadata.create_all(engine)
