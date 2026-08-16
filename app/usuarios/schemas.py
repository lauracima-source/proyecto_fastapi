# app/usuarios/schemas.py
from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    # Field(...) indica que el campo es obligatorio.
    id: int = Field(..., gt=0, description="El ID debe ser mayor a 0")
    username: str = Field(..., min_length=5, description="Mínimo 5 caracteres")
    edad: int = Field(..., ge=18, description="La edad debe ser mayor o igual a 18")

class UsuarioResponse(BaseModel):
    id: int
    username: str
    edad: int
    buscar: str = "general"