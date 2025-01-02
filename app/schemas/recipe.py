from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class RecipeBase(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None

class Recipe(BaseModel):
    id: int
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: str
    created_at: str
    updated_at: str

    @field_validator('cost', mode='before')
    @classmethod
    def convert_cost_to_str(cls, v) -> str:
        return str(v)

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def format_datetime(cls, v: datetime) -> str:
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return v

    class Config:
        from_attributes = True

class RecipeList(BaseModel):
    id: int
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: str

    @field_validator('cost', mode='before')
    @classmethod
    def convert_cost_to_str(cls, v) -> str:
        return str(v)

    class Config:
        from_attributes = True

class RecipeResponse(BaseModel):
    message: str
    recipe: List[Recipe]

class RecipesListResponse(BaseModel):
    recipes: List[RecipeList]

class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    message: str
    required: str = "title, making_time, serves, ingredients, cost"
