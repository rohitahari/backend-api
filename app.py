from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Backend running"}


@app.post("/items")
def create_item(name: str):
    db = SessionLocal()
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item


@app.get("/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        db.close()
        return {"error": "Item not found"}

    item.name = name
    db.commit()
    db.refresh(item)
    db.close()
    return item





@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        db.close()
        return {"error": "Item not found"}

    db.delete(item)
    db.commit()
    db.close()
    return {"message": "Item deleted"}
