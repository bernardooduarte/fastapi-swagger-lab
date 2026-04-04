from fastapi import APIRouter

from app.models import Item, ItemResponse

router = APIRouter(tags=["items"])

@router.get("/items")
def read_items(skip: int = 0, limit: int = 10):
       items = [
           {"id": 1, "name": "Item 1"},
           {"id": 2, "name": "Item 2"},
           {"id": 3, "name": "Item 3"},
           {"id": 4, "name": "Item 4"},
           {"id": 5, "name": "Item 5"},
       ]
       return items[skip : skip + limit]

@router.post("/items", response_model=ItemResponse)
def create_item(item: Item):
       return ItemResponse(
           id=1,
           name=item.name,
           price=item.price,
           in_stock=item.in_stock,
       )