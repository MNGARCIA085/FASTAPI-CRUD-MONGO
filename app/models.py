import uuid
from typing import Optional,List
from pydantic import BaseModel, Field




class Item(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str




class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)
    items: List[Item] = [] # this was like FK????? because of the id I put on Item
    # otra opc. es poner acá otro object_id

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "...",
                "items":[{"name":"bla"}]
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]
    items: List[Item] = []

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes...",
                "items":[{"name":"bla"}]
            }
        }