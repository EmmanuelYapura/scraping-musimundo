from fastapi import FastAPI, BackgroundTasks
import requests
from bs4 import BeautifulSoup

COOKIES = {
    'anonymous-consents': '%5B%5D',
    'cookie-notification': 'NOT_ACCEPTED',
    'ROUTE': '.accstorefront-dd875779d-k6w7s',
    'JSESSIONID': '8161FB0ABC5CBA04FE8297D6EA0BE26E.accstorefront-dd875779d-k6w7s',
    'HSESSION': '1',
}

HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'es-AR,es;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://www.musimundo.com/search/?q=televisores',
    'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

URL = 'https://www.musimundo.com'

def extraer_datos(lista):
    datos = []
    for producto in lista:
        try:
            info_producto = {
                "name": producto["name"],
                "description": producto["description"],
                "cashPrice": producto["cashPrice"]["value"], #Este es el precio base
                "price": producto["price"]["value"], #Precio con descuento (Si es que tiene)
                "onlyDelivery": producto["onlyDelivery"],
                "brandInfo": producto["brandInfo"]["name"],
                "url" : producto["url"]
            }
            datos.append(info_producto)
        except KeyError as e:
            print(f"Producto incompleto, falta {e}")
            continue
    return datos

def extraer_productos_categorias(link, cant_pages, prod):
     for i in range(1, cant_pages):
            params = {
                'q': ':relevance',
                'page': i,
              }
            response = requests.get(link, params=params, cookies=COOKIES, headers=HEADERS)
            data = response.json()
            productos = extraer_datos(data["results"])
            prod.extend(productos)
            print(f'Cantidad de productos scrapeados:  {len(prod)}')

def get_links():
    response = requests.get(URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    #Estos links obtienen todos los de categoria (elementos repetidos)
    links = [a['href'] for a in soup.select('div.ex-h1.nav-submenu-title a')]
    #Los links comienzan a repetirse a partir del elemento 14
    links_sin_repetidos = links[:14]
    return links_sin_repetidos

def buscar_categoria(categoria_url, links):
    categorias = [categoria.split('/')[1] for categoria in links]
    for i in range(len(categorias)):
        if categoria_url == categorias[i]:
            return links[i]
    return False

def productos_cat(nombre_categoria):
    links_cat = get_links()
    link_cat = buscar_categoria(nombre_categoria, links_cat)
    if link_cat:
        url_link = URL + link_cat + '/results'
        params = {
            'q': ':relevance',
            'page': 0,
        }
        response = requests.get(url_link, params=params, cookies=COOKIES, headers=HEADERS)
        data = response.json()
        nro_pages = data["pagination"]["numberOfPages"]
        productos_cat = extraer_datos(data["results"]) 
        extraer_productos_categorias(url_link, nro_pages, productos_cat)
        return productos_cat
    else:
        return {"message": "Esta categoria no tiene productos"}

#FastAPI
app = FastAPI()

@app.get('/')
def index():
    return {"message": "FastAPI esta funcionando correctamente, listar rutas"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

""" @app.get('/productos')
def get_all_products():
    return {"message": "No hay productos que mostrar, vaya a la ruta /scraping para obtener"}

@app.get('/scraping')
def scraping_products(backgound_tasks : BackgroundTasks):
    return {"message": "Se estan generando los productos, esto puede tomar unos minutos, en breve puede volver a /productos"} """

#Retorna las categorias
@app.get('/categorias')
def get_categorias():
    categorias = get_links()
    categorias = [categoria.split('/')[1] for categoria in categorias]
    return categorias

@app.get('/categorias/{nombre_categoria}')
def get_products_cat(nombre_categoria):
    try:
        productos = productos_cat(nombre_categoria)
        return productos
    except Exception as e:
        return {"message": f"No se encontraron productos en la categoria {nombre_categoria}, error: {e}"}

@app.get('/categorias/{nombre_categoria}/{prod_id}')
def get_products_cat(nombre_categoria, prod_id: int):
    try:    
        productos = productos_cat(nombre_categoria)
        return productos[prod_id]
    except Exception as e:
        return {"message": f"No existe el producto con ese id {prod_id} de la categoria {nombre_categoria}, error:  {e}"}
