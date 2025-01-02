from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union
from app.core.database import get_db
from app.models.recipe import Recipe
from app.schemas.recipe import (
    RecipeUpdate,
    RecipeResponse,
    RecipesListResponse,
    MessageResponse,
    ErrorResponse
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"health": "OK"}

@router.post("/recipes", response_model=Union[RecipeResponse, ErrorResponse])
async def create_recipe(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    if not all(field in body for field in required_fields):
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Recipe creation failed!",
                    "required": "title, making_time, serves, ingredients, cost"
                }
            )
    try:
        db_recipe = Recipe(
            title=body['title'],
            making_time=body['making_time'],
            serves=body['serves'],
            ingredients=body['ingredients'],
            cost=body['cost']
        )
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return {
            "message": "Recipe successfully created!",
            "recipe": [db_recipe]
        }
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=200,
            content={
                "message": "Recipe creation failed!",
                "required": "title, making_time, serves, ingredients, cost"
            }
        )

@router.get("/recipes", response_model=RecipesListResponse)
def list_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return {"recipes": recipes}

@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {
        "message": "Recipe details by id",
        "recipe": [recipe]
    }

@router.patch("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe_update: RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = recipe_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recipe, key, value)

    try:
        db.commit()
        db.refresh(db_recipe)
        return {
            "message": "Recipe successfully updated!",
            "recipe": [db_recipe]
        }
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Recipe update failed")

@router.delete("/recipes/{recipe_id}", response_model=MessageResponse)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        return {"message": "No recipe found"}

    try:
        db.delete(db_recipe)
        db.commit()
        return {"message": "Recipe successfully removed!"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Recipe deletion failed")
