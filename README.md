# Recipes API

A RESTful API for managing recipes built with FastAPI and PostgreSQL.

## Features

- Create, read, update, and delete recipes
- Input validation using Pydantic models
- PostgreSQL database with SQLAlchemy ORM
- Environment-based configuration
- RESTful API endpoints

## Requirements

- Python 3.8+
- PostgreSQL
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd recipes-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.template .env
```
Edit `.env` file with your PostgreSQL credentials:
```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=recipes_db
```

5. Create the database in PostgreSQL:
```sql
CREATE DATABASE recipes_db;
```

## Running the Application

Start the application using uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

After starting the application, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

### API Endpoints

#### Create Recipe
- **POST** `/recipes`
- Request Body:
```json
{
  "title": "string",
  "making_time": "string",
  "serves": "string",
  "ingredients": "string",
  "cost": integer
}
```
- Success Response (201):
```json
{
  "message": "Recipe successfully created!",
  "recipe": [
    {
      "id": "1",
      "title": "Chicken Curry",
      "making_time": "45 min",
      "serves": "4 people",
      "ingredients": "onion, chicken, seasoning",
      "cost": "1000",
      "created_at": "2025-01-02 07:29:48",
      "updated_at": "2025-01-02 07:29:48"
    }
  ]
}
```

#### List Recipes
- **GET** `/recipes`
- Success Response (200):
```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Chicken Curry",
      "making_time": "45 min",
      "serves": "4 people",
      "ingredients": "onion, chicken, seasoning",
      "cost": "1000"
    }
  ]
}
```

#### Get Recipe
- **GET** `/recipes/{id}`
- Success Response (200):
```json
{
  "message": "Recipe details by id",
  "recipe": [
    {
      "id": 1,
      "title": "Chicken Curry",
      "making_time": "45 min",
      "serves": "4 people",
      "ingredients": "onion, chicken, seasoning",
      "cost": "1000"
    }
  ]
}
```

#### Update Recipe
- **PATCH** `/recipes/{id}`
- Request Body (all fields optional):
```json
{
  "title": "string",
  "making_time": "string",
  "serves": "string",
  "ingredients": "string",
  "cost": integer
}
```
- Success Response (200):
```json
{
  "message": "Recipe successfully updated!",
  "recipe": [
    {
      "title": "Updated Recipe",
      "making_time": "30 min",
      "serves": "2 people",
      "ingredients": "updated ingredients",
      "cost": "500"
    }
  ]
}
```

#### Delete Recipe
- **DELETE** `/recipes/{id}`
- Success Response (200):
```json
{
  "message": "Recipe successfully removed!"
}
```

## Project Structure
```
recipes_api/
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── recipe.py
│   └── schemas/
│       ├── __init__.py
│       └── recipe.py
│
└── main.py
```

## Error Handling

The API includes proper error handling for common scenarios:
- Invalid input data
- Recipe not found
- Database connection errors
- Validation errors

Error responses include appropriate HTTP status codes and descriptive messages.

## Development

### Code Style
This project follows PEP 8 guidelines for Python code.
