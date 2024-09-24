from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uvicorn
import models
from models import Guitar
from database import engine, Session

app = FastAPI(
    title="Stratolog",
    description="A web application to manage and document your guitar collection.",
    version="0.1.0")
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")



# Input Validation *
class GuitarBase(BaseModel):
    id: Optional[int] = None
    brand: str
    model: str
    year: str
    imagePath: str

class GuitarUpdateBase(BaseModel):
    id: Optional[int] = None
    brand: Optional[str]
    model: Optional[str]
    year: Optional[str]
    imagePath: Optional[str]

# Database Connection/Session Object *
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()



# Page Routes
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/details")
def details(request: Request):
    return templates.TemplateResponse("details.html", {"request": request})

@app.get("/edit")
def edit(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})



# JSON Routes
@app.get("/guitars", status_code=status.HTTP_200_OK)
def readAll():
    with Session() as session:
        guitars = session.query(Guitar).all()
        if guitars is not None:
            return guitars
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@app.get("/guitars/{id}", status_code=status.HTTP_200_OK)
def readById(id: int):
    with Session() as session:
        guitar = session.query(Guitar).filter(Guitar.id == id).first() 
        if guitar is not None:
            return guitar
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} Invalid ID")

@app.post("/guitars", status_code=status.HTTP_201_CREATED)
def create(guitar: GuitarBase):
    with Session() as session:
        newGuitar = models.Guitar(**guitar.model_dump()) # REVIEW
        session.add(newGuitar)
        session.commit()
        return newGuitar

@app.put("/guitars/{id}", status_code=status.HTTP_200_OK)
def update(id: int, guitar: GuitarUpdateBase):
    with Session() as session:
        updatedGuitar = session.query(Guitar).filter(Guitar.id == id).first()
        if updatedGuitar is not None:
            updatedGuitar.brand = guitar.brand
            updatedGuitar.model = guitar.model
            updatedGuitar.year = guitar.year
            updatedGuitar.imagePath = guitar.imagePath
            session.add(updatedGuitar)
            session.commit()
            return updatedGuitar
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} Invalid ID")

@app.delete("/guitars/{id}", status_code=status.HTTP_200_OK)
def delete(id: int):
    with Session() as session:
        guitar = session.query(Guitar).filter(Guitar.id == id).first()
        if guitar is not None:
            session.delete(guitar)
            session.commit()
            return guitar
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} Delete Failed")
    


if __name__ == "__main__":
    uvicorn.run(app, reload=True)