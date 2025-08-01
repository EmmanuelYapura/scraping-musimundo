from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.scraper.musimundo_scraper import MusimundoScrapper
from app.database.schemas.schema import ProductoSchema
from app.database.database import get_base
from app.database.crud.crud import get_or_create_categoria, get_or_create_subcategoria, create_productos

router = APIRouter()
scraper = MusimundoScrapper()

@router.get('/categorias')
def get_categorias():
    return scraper.obtener_subcategorias()

@router.get('/categorias/{nombre_categoria}')
def get_products_cat(nombre_categoria):
    try:
        nombre_categoria = nombre_categoria.lower()
        productos = scraper.obtener_productos_por_categoria(nombre_categoria)
        return productos
    except Exception as e:
        return {"message": f"No se encontraron productos en la categoria {nombre_categoria}, error: {e}"}

@router.get('/categorias/{nombre_categoria}/{subcategoria}')
def get_products_subcategorias(subcategoria):
    try:
        subcategoria = subcategoria.lower()
        products_subcat = scraper.obtener_productos_subcategoria(subcategoria)
        return products_subcat
    except Exception as e:
        return {"message" : f"No se encontraron productos en la subcategoria {subcategoria}, Error {e}"}
    
@router.post('/scraper/{categoria_nombre}')
def scrapear_guardar_productos(categoria_nombre: str, subcategoria_nombre: str = None, db: Session = Depends(get_base)):
    try:
        if subcategoria_nombre:
            productos_data = scraper.obtener_productos_subcategoria(subcategoria_nombre)
        else:
            productos_data = scraper.obtener_productos_por_categoria(categoria_nombre)

        if not productos_data:
            raise HTTPException(status_code=400, detail="Esta categoria no tiene productos")
        
        productos_schema = [ProductoSchema(**data) for data in productos_data]

        categoria = get_or_create_categoria(db, categoria_nombre)

        subcategoria_id = None
        
        if subcategoria_nombre:
            subcategoria = get_or_create_subcategoria(db, subcategoria_nombre, categoria.id)
            subcategoria_id = subcategoria.id

        productos = create_productos(db, productos_schema, categoria.id, subcategoria_id)

        return {
            "message": f"{len(productos)} productos guardados exitosamente",
            "categoria": categoria_nombre,
            "subcategoria": subcategoria_nombre if subcategoria_nombre else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))