# Musimundo Scraper

Este proyecto es un **web scraper** desarrollado en Python que extrae información de productos desde la tienda online de [Musimundo](https://www.musimundo.com/). Se recopilan datos como nombre, descripción, precios, marca y más, y se guardan en archivos `.json` organizados por categoría.

##  Tecnologías utilizadas

  - Python 3
  - requests
  - BeautifulSoup
  - FastAPI

##  ¿Qué hace este scraper?

-  Extrae enlaces únicos de categorías principales.
-  Hace peticiones a la API interna de cada categoría con paginación.
-  Extrae datos relevantes de cada producto:
     -Nombre
     -Descripción
     -Precio original y con descuento
     -Marca
     -Solo envío (booleano)
     -URL del producto
-  Guarda los productos de cada categoría en archivos `.json` con nombre correspondiente.
-  Verifica si el archivo ya existe para evitar sobrescribir datos.

## Cómo ejecutar el scraper

1. **Clonar el repositorio:**

  ```
  git clone https://github.com/EmmanuelYapura/scraping-musimundo.git "nombre_carpeta"
  cd "nombre_carpeta"
  ```

2. **Crear un entorno virtual:**
  ```
  python -m venv venv
  ```
   
- Para Windows
```
venv/Scripts/activate
```
- Para Linux/macOs
```
source venv/bin/activate
```
3. **Instala las dependencias :**
  ```
  pip install -r requirements.txt
  ```
4. **Levantar el servidor**
  ```
  uvicorn main:app --reload
  ```

5. **Ingresar al puerto**
  ```
  http://127.0.0.1:8000
  ```

## Notas importantes

- Este proyecto fue realizado con fines educativos y de práctica en web scraping.
- La estructura de la web puede cambiar y romper el scraper en el futuro.
- Se recomienda evitar hacer peticiones masivas para no sobrecargar los servidores de Musimundo.

## Autor

- **Emmanuel Yapura**  
  [LinkedIn](https://www.linkedin.com/in/emmanuelyapura)
