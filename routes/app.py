from fastapi import APIRouter
from scraper.musimundo_scraper import MusimundoScrapper

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
    