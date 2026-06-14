from fastapi import Query, HTTPException, status
from typing import Annotated

# Función de seguridad para validar el token por Query Parameter
async def verify_api_token(
    token: Annotated[str, Query(description="Token de acceso para la API")]
):
    if token != "nivel-intermedio-2026":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o ausente"
        )
    return token


