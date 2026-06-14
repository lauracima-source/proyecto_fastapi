from fastapi import APIRouter, HTTPException, status, Path, Query, Body
from pydantic import BaseModel, Field
from typing import Annotated

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)

# Base de datos simulada en memoria (Consigna 2)
db_usuarios = []

# Esquema de validación con Pydantic
class Usuario(BaseModel):
    id: int
    username: str = Field(..., min_length=5, description="Mínimo 5 caracteres")
    edad: int = Field(..., ge=18, description="Mínimo 18 años")

# Ejercicio 1: Registro de Usuarios
@router.post("/", status_code=status.HTTP_201_CREATED)
async def registrar_usuario(usuario: Annotated[Usuario, Body()]):
    # Recorrer la lista primero para ver si ya existe (Consigna 2)
    for u in db_usuarios:
        if u["username"] == usuario.username or u["id"] == usuario.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El usuario ya se encuentra registrado"
            )
    
    nuevo_usuario = usuario.model_dump()
    db_usuarios.append(nuevo_usuario)
    return {"mensaje": "Usuario registrado con éxito", "usuario": nuevo_usuario}

# Ejercicio 2: Búsqueda con Rangos (Path + Query)
@router.get("/{user_id}")
async def buscar_usuario(
    user_id: Annotated[int, Path(title="ID del usuario", gt=0)],
    categoria: Annotated[str, Query(min_length=3)] = "general"
):
    for u in db_usuarios:
        if u["id"] == user_id:
            return {
                "usuario": u,
                "categoria_busqueda": categoria
            }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Usuario no encontrado"
    )