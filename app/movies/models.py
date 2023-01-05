import uuid
from typing import Literal, Optional,List
from pydantic import BaseModel, Field


# interesante: https://stackoverflow.com/questions/73136966/how-to-set-range-and-value-out-of-range-in-pydantic-field-using-fastapi






from pydantic import BaseModel, Field as PydanticField
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")













# va a estar embebido en movies
class Review(BaseModel):
    text: str = Field(...)
    score: int = Field(ge=1, le=5) #  pensamiento: (puedo hacer un range de str y luego un list de eso..)






#https://stackoverflow.com/questions/61238502/how-to-require-predefined-string-values-in-python-pydantic-basemodels

class Movie(BaseModel):
    #id: str = Field(default_factory=uuid.uuid4, alias="_id")
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


        


class MovieUpdate(BaseModel):
    title: str = Field(...)
    genres: Optional[List[Literal['action', 'drama','comedy']]]

    class Config:
        schema_extra = {
            "example": {
                "title": "Mad Max the road warrior",
                "genres":['action','drama'],
            }
        }



class MovieOut(Movie):
    _id: ObjectId()
    reviews: Optional[List[Review]] = []

