from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, Base, engine
from models import Product, CartItem
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from decimal import Decimal
from models import CartItem

# Inicializar la aplicación
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# la carpeta "images" para servir archivos estáticos
app.mount("/images", StaticFiles(directory="images"), name="images")

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app para listar productos
@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

class CartItemBase(BaseModel):
    product_id: int
    name: str
    price: Decimal
    quantity: int

class CartItemSchema(BaseModel):
    product_id: int
    quantity: int

# app para agregar un producto al carrito
@app.post("/api/cart")
async def add_to_cart(cart_items: List[CartItemBase], db: Session = Depends(get_db)):
    for item in cart_items:
        # Convertir el precio a Decimal
        item.price = Decimal(str(item.price))
        db_item = db.query(CartItem).filter(CartItem.product_id == item.product_id).first()
        if db_item:
            db_item.quantity = item.quantity
        else:
            db_item = CartItem(
                product_id=item.product_id,
                name=item.name,
                price=item.price,
                quantity=item.quantity
            )
            db.add(db_item)
    db.commit()
    return {"message": "Carrito actualizado correctamente"}

#app para borrar productos del carrito
@app.delete("/api/cart/{product_id}")
async def remove_cart_item(product_id: int, db: Session = Depends(get_db)):
    # Buscar el ítem en la base de datos
    cart_item = db.query(CartItem).filter(CartItem.product_id == product_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="El producto no existe en el carrito")

    # Eliminar el ítem
    db.delete(cart_item)
    db.commit()

    return {"message": "Producto eliminado del carrito"}

#app para actualizar cantidades de los productos en el carrito
@app.put("/api/cart")
async def update_cart(items: List[CartItemSchema], db: Session = Depends(get_db)):
    for item in items:
        db_item = db.query(CartItem).filter(CartItem.product_id == item.product_id).first()
        if db_item:
            # Actualiza la cantidad si el producto ya existe en el carrito
            db_item.quantity = item.quantity
        else:
            # Agrega un nuevo producto si no existe en el carrito
            new_item = CartItem(product_id=item.product_id, quantity=item.quantity)
            db.add(new_item)
    db.commit()
    return {"message": "Cart updated successfully"}