from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)

    subcategorias = relationship("Subcategoria", back_populates="categoria", cascade="all, delete-orphan")

class Subcategoria(Base):
    __tablename__ = 'subcategorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    categoria = relationship("Categoria", back_populates="subcategorias")
    productos = relationship("Producto", back_populates="subcategoria")

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    cashPrice = Column(Float)
    price = Column(Float)
    onlyDelivery = Column(Boolean)
    brandInfo = Column(String)
    url = Column(String)

    subcategoria_id = Column(Integer, ForeignKey('subcategorias.id'))
    subcategoria = relationship("Subcategoria", back_populates="productos")

    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=True)
    categoria = relationship("Categoria", backref="productos_directos")  
    