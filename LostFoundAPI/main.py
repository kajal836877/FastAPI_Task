from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select

from database import engine, get_session
from models import Item
from schemas import ItemCreate, ItemUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


# Create item
@app.post("/items")
def create_item(
    item_data: ItemCreate,
    session: Session = Depends(get_session)
):
    item = Item(
        title=item_data.title,
        description=item_data.description,
        category=item_data.category,
        location=item_data.location,
        reported_by=item_data.reported_by,
        status=item_data.status
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# Get all items
@app.get("/items")
def get_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()

    return items


# Get item by ID
@app.get("/items/{item_id}")
def get_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# Update item
@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item.title = item_data.title
    item.description = item_data.description
    item.category = item_data.category
    item.location = item_data.location
    item.reported_by = item_data.reported_by
    item.status = item_data.status

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# Delete item
@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = session.get(Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    session.delete(item)
    session.commit()

    return {"message": "Item deleted successfully"}


# Get items by status
@app.get("/items/status/{status}")
def get_by_status(
    status: str,
    session: Session = Depends(get_session)
):
    if status not in ["Lost", "Found", "Returned"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Lost, Found or Returned"
        )

    items = session.exec(
        select(Item).where(Item.status == status)
    ).all()

    return items


# Get items by category
@app.get("/items/category/{category}")
def get_by_category(
    category: str,
    session: Session = Depends(get_session)
):
    items = session.exec(
        select(Item).where(Item.category == category)
    ).all()

    return items