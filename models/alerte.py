from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base
from connexion import engine

Base = declarative_base()

class Alerte(Base):
    __tablename__ = "Alerte"
    id_alerte = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)

Base.metadata.create_all(engine)
