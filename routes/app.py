from fastapi import APIRouter
from scraper.musimundo_scraper import MusimundoScrapper

router = APIRouter()
scraper = MusimundoScrapper()

@router.get('/categorias')
def get_categorias():
    return scraper.get_subcategorias()

@router.get('/categorias/{nombre_categoria}')
def get_products_cat(nombre_categoria):
    try:
        nombre_categoria = nombre_categoria.lower()
        productos = scraper.productos_cat(nombre_categoria)
        return productos
    except Exception as e:
        return {"message": f"No se encontraron productos en la categoria {nombre_categoria}, error: {e}"}

@router.get('/categorias/{nombre_categoria}/{subcategoria}')
def get_products_subcategorias(subcategoria):
    try:
        subcategoria = subcategoria.lower()
        products_subcat = scraper.get_products_subCat(subcategoria)
        return products_subcat
    except Exception as e:
        return {"message" : f"No se encontraron productos en la subcategoria {subcategoria}, Error {e}"}
    