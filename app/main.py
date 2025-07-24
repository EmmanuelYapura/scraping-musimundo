from fastapi import FastAPI
from app.routes.app import router
from app.database.database import Base, engine
from app.constantes import description


app = FastAPI(
    title="MusimundoScraper API",
    description=description,
    summary="API para scraping y gestión de productos de Musimundo.",
    version="1.0.0",
    contact={
        "name": "Repository",
        "url": "https://github.com/EmmanuelYapura/scraping-musimundo",
        "email": "eyapura96@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)
Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.get('/')
def index():
    return {"message": "FastAPI esta funcionando correctamente. Rutas: /categorias, /categorias/{nombre}, /categorias/{nombre}/{subcategoria}"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
