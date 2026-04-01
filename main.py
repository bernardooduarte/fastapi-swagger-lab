from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Swagger!"}

@app.get("/hello/{name}")
def read_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    items = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"},
        {"id": 4, "name": "Item 4"},
        {"id": 5, "name": "Item 5"},
    ]
    return items[skip : skip + limit]