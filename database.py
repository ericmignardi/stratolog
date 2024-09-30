from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/Stratolog")

Base = declarative_base()

Session = sessionmaker(bind=engine, expire_on_commit=False)