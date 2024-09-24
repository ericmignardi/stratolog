from sqlalchemy import Column, Integer, String
from database import Base

# Data Model & Object Relational Mapping
class Guitar(Base):
    __tablename__ = 'guitar'
    id = Column("id", Integer, primary_key=True, index=True)
    brand = Column("brand", String(25), nullable=False)
    model = Column("model", String(50), nullable=False)
    year = Column("year", String(4), nullable=False)
    colour = Column("colour", String(25), nullable=False)
    type = Column("type", String(25), nullable=False)