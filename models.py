from sqlalchemy import Column, Integer, String
from database import Base

# Data Model & Object Relational Mapping
class Guitar(Base):
    __tablename__ = 'guitar'
    id = Column("id", Integer, primary_key=True, index=True)
    brand = Column("brand", String(20), nullable=False)
    model = Column("model", String(20), nullable=False)
    year = Column("year", String(4), nullable=False)
    imagePath = Column("imagePath", String(20), nullable=False)