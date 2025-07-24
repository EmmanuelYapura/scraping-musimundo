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

def create_productos(db: Session, productos_data: list[ProductoSchema], categoria_id: int, subcategoria_id: int = None):
    for producto in productos_data:
        producto_existente = db.query(Producto).filter(Producto.url == producto.url).first()

        if producto_existente:
            producto_existente.name = producto.name
            producto_existente.price = producto.price
            producto_existente.cashPrice = producto.cashPrice
            producto_existente.onlyDelivery = producto.onlyDelivery
            producto_existente.brandInfo = producto.brandInfo
            producto_existente.description = producto.description
            producto_existente.categoria_id = categoria_id

            # Solo actualiza subcategoria si estaba vacía
            if not producto_existente.subcategoria_id and subcategoria_id:
                producto_existente.subcategoria_id = subcategoria_id
        
        else:
            nuevo = Producto(
                name = producto.name,
                description = producto.description,
                cashPrice = producto.cashPrice,
                price = producto.price,
                onlyDelivery = producto.onlyDelivery,
                brandInfo = producto.brandInfo,
                url = producto.url,
                subcategoria_id = subcategoria_id,
                categoria_id = categoria_id
            )
            db.add(nuevo)
    db.commit()

    return productos_data
    