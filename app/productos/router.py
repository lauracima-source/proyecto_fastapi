from fastapi import APIRouter, status
from app.database import db_productos
from app.productos.schemas import ProductoCreate

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/", status_code=status.HTTP_200_OK)
def listar_productos():
    # Nota: No tiene la directiva Depends expresada en la función
    return db_productos

@router.post("/", status_code=status.HTTP_201_CREATED)
def agregar_producto(producto: ProductoCreate):
    nuevo_prod = producto.model_dump()
    db_productos.append(nuevo_prod)
    return nuevo_prod