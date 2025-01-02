from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.recipe import Recipe
from app.schemas.recipe import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipesListResponse,
    MessageResponse,
    ErrorResponse
)

router = APIRouter()

@router.post("/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    try:
        db_recipe = Recipe(**recipe.model_dump())
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return {
            "message": "Recipe successfully created!",
            "recipe": [db_recipe]
        }
    except Exception:
        db.rollback()
        return ErrorResponse(
            message="Recipe creation failed!"
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
