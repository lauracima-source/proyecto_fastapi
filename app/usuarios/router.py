from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, status
from app.database import db_usuarios
from app.usuarios.schemas import UsuarioCreate

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# Endpoint POST: Registro de Usuario
@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate):
    # Control de duplicados por ID o por Username
    for u in db_usuarios:
        if u["id"] == usuario.id or u["username"] == usuario.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario o ID ya existe en la base de datos."
            )
    
    nuevo_usuario = usuario.model_dump()
    nuevo_usuario["buscar"] = "general"
    db_usuarios.append(nuevo_usuario)
    return nuevo_usuario

# Endpoint GET: Búsqueda por ID con validación de Path y Query parameter
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def buscar_usuario_por_id(
    user_id: Annotated[int, Path(gt=0, description="El user_id debe ser estrictamente mayor a 0")],
    buscar: str = Query("general", description="Valor de búsqueda por defecto 'general'")
):
    for u in db_usuarios:
        if u["id"] == user_id:
            resultado = dict(u)
            resultado["buscar"] = buscar
            return resultado
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )
