import uuid
from typing import Literal, Optional,List
from pydantic import BaseModel, Field

class Prueba(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    genres: Optional[List[Literal['action', 'drama','comedy']]]


    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Mad Max",
                "genres":['action','comedy'],
            }
        }


