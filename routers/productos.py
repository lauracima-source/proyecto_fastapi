from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from dependencies import verify_api_token

router = APIRouter(
    prefix="/products",
    tags=["Productos"]
)

# Base de datos simulada de productos
db_productos = []

class Producto(BaseModel):
    nombre: str
    precio: float

# Ejercicio 3: Inyección de Dependencias Externas (POST protegido)
@router.post("/", status_code=201)
async def agregar_producto(
    producto: Producto,
    token: Annotated[str, Depends(verify_api_token)]
):
    nuevo_prod = producto.model_dump()
    db_productos.append(nuevo_prod)
    return {"mensaje": "Producto agregado", "producto": nuevo_prod}

# Ejercicio 4: Validación Final (Listar todo sin Depends manual)
@router.get("/")
async def listar_productos():
    return db_productos
