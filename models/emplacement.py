from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class Emplacement(Base):
    __tablename__ = "Emplacement"
    id_emplacement = Column(Integer, primary_key=True)
    nom_emplacement = Column(String(50), nullable=False)
    type_emplacement = Column(String(50), nullable=False)

Base.metadata.create_all(engine)
