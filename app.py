from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel

app = FastAPI(
    title="Stratolog",
    description="A web application to manage and document your guitar collection.",
    version="0.1.0")

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/Stratolog")
Base = declarative_base()
Session = sessionmaker(bind=engine)

templates = Jinja2Templates(directory="templates")



class GuitarModel(BaseModel):
    id: int
    brand: str
    model: str
    year: str
    imagePath: str



# Data Model & Mapping
class Guitar(Base):
    __tablename__ = "guitar"
    id = Column("id", Integer, primary_key=True)
    brand = Column("brand", String(20), nullable=False)
    model = Column("model", String(20), nullable=False)
    year = Column("year", String(4), nullable=False)
    imagePath = Column("imagePath", String(255), nullable=False)
    def __repr__(self):
        return f"<Guitar(Id: {self.id}, Brand: {self.brand}, Model: {self.model}, Year: {self.year}, ImagePath: {self.imagePath}>"

def main() -> None:
    Base.metadata.create_all(engine)



# Page Endpoints
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/details")
def details(request: Request):
    return templates.TemplateResponse("details.html", {"request": request})

@app.get("/edit")
def edit(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})



# JSON Endpoints
@app.get("/guitars")
def readAll(request: Request):
    with Session() as session:
        return session.query(Guitar).all()
    
@app.get("/guitars/{id}")
def readById(request: Request, id: int):    
    with Session() as session:
        return session.query(Guitar).get(id)
    
@app.post("/guitars", status_code=201)
def create(request: Request, guitar: GuitarModel):
    with Session() as session:
        session.add(guitar)
        session.commit()
        return "Create Success"

# @app.put("/guitars/{id}")
# def update(request: Request, id: int, guitar: Guitar):
#     return "Not Implemented"

@app.delete("/guitars/{id}")
def delete(request: Request, id: int):
    with Session() as session:
        guitar = session.query(Guitar).get(id)
        session.delete(guitar)
        session.commit()
        return "Delete Success"
    


if __name__ == "__main__":
    main()