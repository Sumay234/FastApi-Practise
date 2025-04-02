from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
data = []

class Book(BaseModel):
    title: str
    author: str
    publisher: str

@app.post("/book")
def create_book(book:Book):
    data.append(book.dict())
    return data

@app.get("/{id}")
def read_book(id:int):
    return data[id]

# edit 
@app.put("book/{id}")
def updatebook(id:int, book: Book):
    data[id] = book
    return book