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

    def extraer_productos_categorias(self, link, cant_pages, prod):
        for i in range(1, cant_pages):
                params = {
                    'q': ':relevance',
                    'page': i,
                }
                response = requests.get(link, params=params, cookies=self.COOKIES, headers=self.HEADERS)
                data = response.json()
                prod.extend(self.extraer_datos(data["results"]))
                print(f'Cantidad de productos scrapeados:  {len(prod)}')

    def scrapear_productos_por_url(self, url):
        try:
            params = {'q': ':relevance', 'page': 0}
            response = requests.get(url, params=params, cookies=self.COOKIES, headers=self.HEADERS)
            data = response.json()
            nro_pages = data["pagination"]["numberOfPages"]
            productos = self.extraer_datos(data["results"])
            self.extraer_productos_categorias(url, nro_pages, productos)
            return productos
        except Exception as e:
            raise {"message": f"Error al scrapear productos: {e}"}

    """ Categorias """
    def get_links(self):
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

    def productos_cat(self, nombre_categoria):
        links_cat = self.get_links()
        link_cat = self.buscar_categoria(nombre_categoria, links_cat)
        if link_cat:
            url_link = self.URL + link_cat + '/results'
            return self.scrapear_productos_por_url(url_link)
        else:
            return {"message": "Esta categoria no tiene productos o no existe"}

    """ Subcategorias """
    def get_subcategorias(self, url = False):
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.text, "html.parser")
        #Estos contenedores son de cada categoria principal
        contenedores_cat = soup.find_all('div', class_='mus-nav-Lc')
        subcategorias = []

        for categoria in contenedores_cat:
            nombre_categoria = categoria.find('div', class_='ex-h2')
            categoria_principal = nombre_categoria.find('a')["href"].split('/')[1]
            item = {"categoria" : categoria_principal, "subcategorias": []}
            #Contenedores subcategorias
            ul_list = categoria.find_all('ul')
            for ul in ul_list:
                #obtengo los links de subcategorias
                link = ul.find_all('a')
                for subcat in link:
                    nombre = subcat.text.strip().replace(' ', '-').lower()
                    url_api = f'/categorias/{categoria_principal}/{nombre}'
                    item['subcategorias'].append({"nombre": nombre.lower(), "url": subcat["href"] if url else url_api})
            subcategorias.append(item)
        return subcategorias

    def buscar_subCategoria(self, sub_categoria, lista_categorias):
        for categoria in lista_categorias:
            for subcategoria in categoria["subcategorias"]:
                if sub_categoria == subcategoria["nombre"]:
                    return subcategoria["url"]
        return False

    def get_products_subCat(self, subCategoria):
        all_categorias = self.get_subcategorias(True)
        link_subCat = self.buscar_subCategoria(subCategoria, all_categorias)
        if link_subCat:
            url_link = URL + link_subCat + '/results'
            return self.scrapear_productos_por_url(url_link)
        else:
            return {"message": "Esta categoria no tiene productos o no existe"}
