import requests
from bs4 import BeautifulSoup
from constantes import URL,COOKIES,HEADERS 

class MusimundoScrapper():
    URL = URL
    COOKIES = COOKIES
    HEADERS = HEADERS

    def __init__(self):
        pass

    def extraer_datos(self, lista):
        datos = []
        for producto in lista:
            try:
                datos.append({
                    "name": producto["name"],
                    "description": producto["description"],
                    "cashPrice": producto["cashPrice"]["value"], #Este es el precio base
                    "price": producto["price"]["value"], #Precio con descuento (Si es que tiene)
                    "onlyDelivery": producto["onlyDelivery"],
                    "brandInfo": producto["brandInfo"]["name"],
                    "url" : producto["url"]
                })
            except KeyError as e:
                print(f"Producto incompleto, falta {e}")
                continue
        return datos

    def extraer_productos_categorias(self, link, cant_paginas, productos):
        for i in range(1, cant_paginas):
                params = {
                    'q': ':relevance',
                    'page': i,
                }
                response = requests.get(link, params=params, cookies=self.COOKIES, headers=self.HEADERS)
                data = response.json()
                productos.extend(self.extraer_datos(data["results"]))
                print(f'Cantidad de productos scrapeados:  {len(productos)}')

    def scrapear_productos_por_url(self, url):
        try:
            params = {'q': ':relevance', 'page': 0}
            response = requests.get(url, params=params, cookies=self.COOKIES, headers=self.HEADERS)
            data = response.json()
            total_paginas = data["pagination"]["numberOfPages"]
            productos = self.extraer_datos(data["results"])
            self.extraer_productos_categorias(url, total_paginas, productos)
            return productos
        except Exception as e:
            raise {"message": f"Error al scrapear productos: {e}"}

    """ Categorias """
    def obtener_links_categorias(self):
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.text, "html.parser")
        #Estos links obtienen todos los de categoria (elementos repetidos)
        links = [a['href'] for a in soup.select('div.ex-h1.nav-submenu-title a')]
        #Los links comienzan a repetirse a partir del elemento 14
        return links[:14]

    def buscar_categoria(self, categoria_url, links):
        categorias = [link.split('/')[1] for link in links]
        for i in range(len(categorias)):
            if categoria_url == categorias[i]:
                return links[i]
        return False

    def obtener_productos_por_categoria(self, nombre_categoria):
        links_cat = self.obtener_links_categorias()
        link_cat = self.buscar_categoria(nombre_categoria, links_cat)
        if link_cat:
            url_link = self.URL + link_cat + '/results'
            return self.scrapear_productos_por_url(url_link)
        else:
            return {"message": "Esta categoria no tiene productos o no existe"}

    """ Subcategorias """
    def obtener_subcategorias(self, url = False):
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.text, "html.parser")
        #Estos contenedores son de cada categoria principal
        contenedores_cat = soup.find_all('div', class_='mus-nav-Lc')
        subcategorias = []

        for categoria in contenedores_cat:
            contenedor_categoria = categoria.find('div', class_='ex-h2')
            nombre_categoria = contenedor_categoria.find('a')["href"].split('/')[1]
            item = {"categoria" : nombre_categoria, "subcategorias": []}
            #Contenedores subcategorias
            ul_list = categoria.find_all('ul')
            for ul in ul_list:
                #obtengo los links de subcategorias
                link = ul.find_all('a')
                for subcat in link:
                    nombre = subcat.text.strip().replace(' ', '-').lower()
                    url_api = f'/categorias/{nombre_categoria}/{nombre}'
                    item['subcategorias'].append({"nombre": nombre.lower(), "url": subcat["href"] if url else url_api})
            subcategorias.append(item)
        return subcategorias

    def buscar_subcategoria(self, nombre_sub_cat, lista_categorias):
        for categoria in lista_categorias:
            for subcategoria in categoria["subcategorias"]:
                if nombre_sub_cat == subcategoria["nombre"]:
                    return subcategoria["url"]
        return False

    def obtener_productos_subcategoria(self, sub_categoria):
        total_categorias = self.obtener_subcategorias(True)
        link_sub_cat = self.buscar_subcategoria(sub_categoria, total_categorias)
        if link_sub_cat:
            url_link = URL + link_sub_cat + '/results'
            return self.scrapear_productos_por_url(url_link)
        else:
            return {"message": "Esta categoria no tiene productos o no existe"}
