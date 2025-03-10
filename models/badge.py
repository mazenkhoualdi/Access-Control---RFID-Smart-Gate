from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class Badge(Base):
    __tablename__ = "Badge"
    
    id_badge = Column(Integer, primary_key=True)
    uid_badge = Column(String(50), nullable=False, unique=True)
    id_employe = Column(Integer, ForeignKey('Employe.id_employe'), nullable=True)  # Si NULL, badge non attribué

    employe = relationship("Employe", back_populates="badge")

Base.metadata.create_all(engine)
