from sqlalchemy.orm import Session
from  database.models.models import Categoria, Subcategoria, Producto
from database.schemas.schema import ProductoSchema

def get_or_create_categoria(db: Session, nombre: str):
    categoria = db.query(Categoria).filter(Categoria.nombre == nombre).first()
    if not categoria:
        categoria = Categoria(nombre=nombre)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
    return categoria

def get_or_create_subcategoria(db: Session, nombre: str, categoria_id: int):
    subcategoria = db.query(Subcategoria).filter(Subcategoria.nombre == nombre, Subcategoria.categoria_id == categoria_id).first()
    if not subcategoria:
        subcategoria = Subcategoria(nombre=nombre, categoria_id=categoria_id)
        db.add(subcategoria)
        db.commit()
        db.refresh(subcategoria)
    return subcategoria

def create_productos(db: Session, productos_data: list[ProductoSchema], subcategoria_id: int = None):
    productos = []
    for data in productos_data:
        producto = Producto(
            name = data.name,
            description = data.description,
            cashPrice = data.cashPrice,
            price = data.price,
            onlyDelivery = data.onlyDelivery,
            brandInfo = data.brandInfo,
            url = data.url,
            subcategoria_id = subcategoria_id
        )
        productos.append(producto)
    db.add_all(productos)
    db.commit()
    return productos