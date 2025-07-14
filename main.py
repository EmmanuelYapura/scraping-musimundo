from fastapi import FastAPI
from routes.app import router
from database.database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.get('/')
def index():
    return {"message": "FastAPI esta funcionando correctamente. Rutas: /categorias, /categorias/{nombre}, /categorias/{nombre}/{subcategoria}"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
