from pydantic import BaseModel, Field

class ProductoCreate(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2)
    precio: float = Field(..., gt=0)