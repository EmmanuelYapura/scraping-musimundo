from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database.database import Base

class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), unique=True, nullable=False)

    subcategorias = relationship("Subcategoria", back_populates="categoria", cascade="all, delete-orphan")

class Subcategoria(Base):
    __tablename__ = 'subcategorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(Text, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    categoria = relationship("Categoria", back_populates="subcategorias")
    productos = relationship("Producto", back_populates="subcategoria")

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    cashPrice = Column(Float)
    price = Column(Float)
    onlyDelivery = Column(Boolean)
    brandInfo = Column(Text)
    url = Column(Text)

    subcategoria_id = Column(Integer, ForeignKey('subcategorias.id'))
    subcategoria = relationship("Subcategoria", back_populates="productos")

    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=True)
    categoria = relationship("Categoria", backref="productos_directos")  
    