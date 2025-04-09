from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class Employe(Base):
    __tablename__ = "Employe"
    
    id_employe = Column(String(50), primary_key=True)  # Modification ici (String(50) au lieu de Integer)
    nom_employe = Column(String(50), nullable=False)
    prenom_employe = Column(String(50), nullable=False)
    id_equipe = Column(Integer, ForeignKey('Equipe.id_equipe'), nullable=False)
    competence = Column(String(50), nullable=False)

    equipe = relationship("Equipe", back_populates="employes")
    badge = relationship("Badge", back_populates="employe", uselist=False)

Base.metadata.create_all(engine)
