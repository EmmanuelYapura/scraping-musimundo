# Musimundo Scraper

Este proyecto es un **web scraper** desarrollado en Python que extrae información de productos desde la tienda online de [Musimundo](https://www.musimundo.com/). Se recopilan datos como nombre, descripción, precios, marca y más, y se guardan en una base de datos mysql organizados por categoría o subcategoria. Tambien pueden visualizarse todos los productos en la tabla productos.

## Tecnologías utilizadas

- Python 3
- requests
- BeautifulSoup
- FastAPI
- SQLAlchemy

## ¿Qué hace este scraper?

- Extrae enlaces únicos de categorías principales.
- Hace peticiones a la API interna de cada categoría con paginación.
- Extrae datos relevantes de cada producto:
  -Nombre
  -Descripción
  -Precio original y con descuento
  -Marca
  -Solo envío (booleano)
  -URL del producto
- Guarda productos en una base de datos mysql, en este proyecto la base de datos tiene un usuaio root y una contrasena hardcodeada para su uso rapido siguiendo las instrucciones
- Verifica si el producto ya existe para evitar sobrescribir datos y actualiza sus id de subcategorias en caso de ser necesario

## Docker (¡rápido y sin instalaciones locales!)

Si solo querés probar o ejecutar el proyecto sin instalar Python ni dependencias, usá Docker.

### 1. Requisitos

- Tener instalado [Docker Engine](https://docs.docker.com/engine/install/) (o Docker Desktop en Windows/Mac).

### 2. Construir la imagen

Desde la **raíz del repo** (donde está el `Dockerfile`):

```bash
   docker build -t musimundo-api .
```

### 3. Levantar el servidor

```bash
   docker run -d --name musimundo-container -p 8000:8000 musimundo-api
```

### 4. Abrir navegador en:

- http://localhost:8000/ – Para visualizar rutas
- http://localhost:8000/categorias – Para visualizar categorias
- http://localhost:8000/docs – Swagger interactivo
- http://localhost:8000/redoc – ReDoc

---

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

4. **Crear base de datos para la conexion**
- Nota: en estas instrucciones vamos a crear la base usando un contenedor mysql en docker y usando un usuario root a modo de prueba. Creamos el contenedor usando la imagen de mysql con la siguiente linea:

```
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 mysql
```

- Ingresar el password para el cliente root para ingresar a la base de datos
- Dentro de la terminal del contenedor de docker:

```
mysql -p
```

- Nota: en la consola de docker la contrasena es invisible!

- Creamos la base de datos

```
CREATE DATABASE test;
```

```
USE test;
```

5. **Levantar el servidor**

```
uvicorn app.main:app --reload
```

6. **Ingresar al puerto**

```
http://127.0.0.1:8000
```

## Endpoints

- GET /categorias

  - Descripcion: Devuelve las categorias junto a sus subcategorias

  - Ejemplo

  ```
  curl http://127.0.0.1:8000/categorias
  ```

  - Respuesta

  ```
  [
    {
      "categoria": "climatizacion",
      "subcategorias": [
        {
          "nombre": "aire-acondicionado",
          "url": "/categorias/climatizacion/aire-acondicionado"
        },
        {
          "nombre": "calefactores",
          "url": "/categorias/climatizacion/calefactores"
        },
        {
          "nombre": "ventiladores",
          "url": "/categorias/climatizacion/ventiladores"
        },
        {
          "nombre": "climatizadores",
          "url": "/categorias/climatizacion/climatizadores"
        },
        {
          "nombre": "accesorios",
          "url": "/categorias/climatizacion/accesorios"
        }
      ]
    },
  ...
  ]
  ```

- GET /categorias/{nombre_categoria}

  - Descripcion: Devuelve una lista de productos de la categoria especificada

  - Parametros

    - nombre_categoria (string)

  - Ejemplo

  ```
  curl http://127.0.0.1:8000/categorias/camaras
  ```

  - Respuesta

  ```
  [
    {
      "name": "CAMARA IP INALAMBRICA NOGANET NGW-45",
      "description": "Camara IP inalambrica. Vision nocturna. 4 LEDS infrarrojos + 4 LEDS blancos. Rotacion 355/90. Resolucion de 480P. Angulo de vision 120. Video H.264. Reproduccion 24/7. Audio bidireccional. Detector de movimiento. Control remoto desde App. Lector Micro SD: 128G. Conexion: WiFi 802.11b/g/n. Montable a la pared. Medidas: (alt x anc x prof): 10 x 10 x 8 cm.",
      "cashPrice": 37999,
      "price": 37999,
      "onlyDelivery": false,
      "brandInfo": "NOGANET",
      "url": "/camaras/camaras-de-seguridad/camara-ip-inalambrica-noganet-ngw-45/p/01092014"
    },
    {
      "name": "CAMARA IP INALAMBRICA NOGANET NGW-11",
      "description": "Camara IP inalambrica. Vision nocturna. 4 LEDS infrarrojos + 4 LEDS blancos. Rotacion 355/90. Resolucion de 480P. Angulo de vision 120. Video H.264. Reproduccion 24/7. Audio bidireccional. Detector de movimiento. Control remoto desde App. Lector Micro SD: 128G. Conexion: WiFi 802.11b/g/n. Montable a la pared. Medidas: (alt x anc x prof): 14 x 11 x 10 cm.",
      "cashPrice": 31999,
      "price": 31999,
      "onlyDelivery": false,
      "brandInfo": "NOGANET",
      "url": "/camaras/camaras-de-seguridad/camara-ip-inalambrica-noganet-ngw-11/p/01092013"
    },
  ...
  ]
  ```

- GET /categorias/{nombre_categoria}/{subcategoria}

  - Descripcion: Devuelve una lista de productos de la subcategoria especificada

  - Parametros

    - nombre_categoria (string)
    - subcategoria (string)

  - Ejemplo

  ```
  curl http://127.0.0.1:8000/categorias/audio-tv-video/televisores
  ```

  - Respuesta

  ```
  [
    {
      "name": "SMART DLED GOOGLE TV QUINT 32\" PULGADAS HD QT3-32 GTV2024 HD",
      "description": "Televisor Smart DLED Google. Pantalla de 32\" HD (1366x768). Frecuncia de barrido 50/60Hz. Radio de contraste 5000:01. Brillo 240 CD/M2. Salidas de audio. Potencia 2 x 10 W (RMS). Conexiones: Wi Fi (2.4G/5G). Bluetooth 5.0. HDMI. USB. Incluye conermoto.",
      "cashPrice": 299999,
      "price": 229999,
      "onlyDelivery": false,
      "brandInfo": "QUINT",
      "url": "/audio-tv-video/televisores/smart-dled-google-tv-quint-32-pulgadas-hd-qt3-32-gtv2024-hd/p/01071002"
    },
    {
      "name": "SMART LED TV PHILIPS 32\" PULGADAS HD 32PHD6910/77",
      "description": "Televisor Smart LED. Pantalla de 32\" Pixel Plus HD (1366x768 px). Relacion de aspecto: 16:9. Tamano diagonal: 80 cm. Frecuencia de barrido: 60 Hz. Brillo 200cd/m2. Contraste y color HDR1. Audio: Dolby Digital MS12 V2.6.2: nivelador de volumen. Modo nocturno. Mejora de graves. Dialogos nitidos. Ecualizador con IA. Sonido con IA. Potencia RMS: 16 W. Sintonizador TDA. Conexiones: Wi-Fi integrada. 3x HDMI. 2x USB. Antena IEC75. Ethernet-LAN RJ-45. Sistema operativo: TITAN. Medidas con base (alt x anch x prof): 71.1 x 17 x 4.38 cm.",
      "cashPrice": 422399,
      "price": 259999,
      "onlyDelivery": false,
      "brandInfo": "PHILIPS",
      "url": "/audio-tv-video/televisores/smart-led-tv-philips-32-pulgadas-hd-32phd6910-77/p/01048006"
    },
  ...
  ]
  ```

- POST /scraper/categoria

  - Descripcion: Carga los productos en la base de datos

  - Ejemplo

  ```
  curl http://127.0.0.1:8000/scraper/electrohogar
  ```

  - Respuesta

  ```
  {
  "message": "497 productos guardados exitosamente",
  "categoria": "electrohogar",
  "subcategoria": null
  }
  ```

## Notas importantes

- Este proyecto fue realizado con fines educativos y de práctica en web scraping.
- La estructura de la web puede cambiar y romper el scraper en el futuro.
- Se recomienda evitar hacer peticiones masivas para no sobrecargar los servidores de Musimundo.
- La base de datos que se utiliza en este proyecto esta hardcodeada con un usuario root, por ese motivo no hay un archivo .env con variables de entorno

## Autor

- **Emmanuel Yapura**  
  [LinkedIn](https://www.linkedin.com/in/emmanuelyapura)
