from fastapi import APIRouter


search_api = APIRouter()


@search_api.get("/", status_code=200)
def read_root():
    return {"message": "Hello, FastAPI!"}