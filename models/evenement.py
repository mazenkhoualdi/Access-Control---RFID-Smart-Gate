from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class Evenement(Base):
    __tablename__ = "Evenement"
    id_event = Column(Integer, primary_key=True)
    id_employe = Column(Integer, ForeignKey("Employe.id_employe"), nullable=False)
    id_equipe = Column(Integer, ForeignKey("Equipe.id_equipe"), nullable=False)
    id_poste = Column(Integer, ForeignKey("Poste_Competence.id_poste"), nullable=False)
    id_alerte = Column(Integer, ForeignKey("Alerte.id_alerte"), nullable=False)
    id_emplacement = Column(Integer, ForeignKey("Emplacement.id_emplacement"), nullable=False)
    date_entree = Column(DateTime, nullable=False)
    date_sortie = Column(DateTime)

Base.metadata.create_all(engine)
