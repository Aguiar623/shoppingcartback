from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Modelo para la tabla "products"
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric, nullable=False)
    image = Column(Text, nullable=False)

# Modelo para la tabla "cart_items"
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # Relación con products
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    product = relationship("Product")  # Relación
