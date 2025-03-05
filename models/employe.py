from sqlalchemy import Column, Integer, String
from connexion import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employe(Base):
    __tablename__ = "Employe"
    id_employe = Column(Integer, primary_key=True)
    nom_Employe = Column(String(50), nullable=False)
    prenom_Employe = Column(String(50), nullable=False)

Base.metadata.create_all(engine)
