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

description = """
**MusimundoScraper API** te permite automatizar el scraping y gestión de productos desde la tienda online de Musimundo.

## Categorías y Subcategorías

- Podés **obtener categorías** y sus respectivas subcategorías.

- Almacenar productos en función de la categoría o subcategoría scrapeada.

## Productos

- Los productos se guardan en base de datos (SQLite).

- Se **actualizan automáticamente** si ya existen, evitando duplicados.

- Se pueden asociar a subcategorías aunque inicialmente se hayan cargado solo con la categoría.

"""