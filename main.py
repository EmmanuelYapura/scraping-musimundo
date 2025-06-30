import requests
from bs4 import BeautifulSoup
import json, os

cookies = {
    'anonymous-consents': '%5B%5D',
    'cookie-notification': 'NOT_ACCEPTED',
    'ROUTE': '.accstorefront-dd875779d-k6w7s',
    'JSESSIONID': '8161FB0ABC5CBA04FE8297D6EA0BE26E.accstorefront-dd875779d-k6w7s',
    'HSESSION': '1',
}

headers = {
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

response = requests.get(URL)

html = response.text
soup = BeautifulSoup(html, "html.parser")

#Estos links obtienen todos los de categoria (elementos repetidos)
links = [a['href'] for a in soup.select('div.ex-h1.nav-submenu-title a')]

#Los links comienzan a repetirse a partir del elemento 14
links_sin_repetidos = links[:14]

def crear_json(nombre, lista):
    carpeta = 'productos'
    os.makedirs(carpeta, exist_ok=True)

    ruta_archivo = os.path.join(carpeta, f"{nombre}.json")

    if os.path.exists(ruta_archivo):
        print(f"El archivo '{nombre}.json' ya existe. No se sobreescribirá.")
        return

    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            json.dump(lista, file, indent=4, ensure_ascii=False)
            print(f"Archivo {nombre}.json creado.")
    except Exception as e:
        print(f" Error al guardar el archivo {nombre}.json: {e}")

def extraer_datos(lista):
    datos = []
    for producto in lista:
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
    return datos

def extraer_productos_categorias(link, cant_pages, prod):
     for i in range(1, cant_pages):
            params = {
                'q': ':relevance',
                'page': i,
              }
            response = requests.get(link, params=params, cookies=cookies, headers=headers)
            data = response.json()
            productos = extraer_datos(data["results"])
            prod = prod + productos
            print(f'Cantidad de productos scrapeados:  {len(prod)}')
    

def scraping_links(links):
    for link in links:
        url_link = URL + link + '/results'

        nombre_categoria = link.split('/')[1]
        print(f"Categoria: {nombre_categoria}")

        params = {
            'q': ':relevance',
            'page': 0,
        }
        response = requests.get(url_link, params=params, cookies=cookies, headers=headers)
        data = response.json()
        nro_pages = data["pagination"]["numberOfPages"]
        productos_cat = extraer_datos(data["results"]) 
        extraer_productos_categorias(url_link, nro_pages, productos_cat)
        
        if productos_cat:
            crear_json(nombre_categoria, productos_cat)
        else:
            print(f"La categoria {nombre_categoria} no tiene productos cargados")

scraping_links(links_sin_repetidos)
