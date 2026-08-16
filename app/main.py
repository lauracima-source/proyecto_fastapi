from fastapi import FastAPI, Depends
from app.usuarios.router import router as router_usuarios
from app.productos.router import router as router_productos
from app.productos.dependencies import verificar_token

app = FastAPI(title="TP2 - Pruebas Automatizadas")

# Enrutador de Usuarios (público)
app.include_router(router_usuarios)

# Enrutador de Productos: Se le aplica Bloqueo Perimetral Global mediante 'dependencies'
app.include_router(
    router_productos,
    dependencies=[Depends(verificar_token)]
)

@app.get("/")
def read_root():
    return {"mensaje": "API de Práctica Profesionalizante I Lista"}
