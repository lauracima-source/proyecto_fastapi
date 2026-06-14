from fastapi import FastAPI, Depends
from routers import usuarios, productos
from dependencies import verify_api_token

app = FastAPI(
    title="Práctica Profesionalizante I - TP1",
    description="Desarrollo modularizado aplicando validaciones con Annotated",
    version="1.0.0"
)

# Ejercicio 4: Incluimos el router de usuarios de forma normal
app.include_router(usuarios.router)

# Ejercicio 4: Incluimos el router de productos aplicando bloqueo global con el parámetro dependencies
app.include_router(
    productos.router,
    dependencies=[Depends(verify_api_token)]
)

@app.get("/")
async def root():
    return {"institucion": "Instituto Técnico Superior Córdoba", "estado": "API Activa"}

