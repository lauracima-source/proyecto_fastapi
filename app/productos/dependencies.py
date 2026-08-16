from fastapi import HTTPException, Query, status

def verificar_token(token: str = Query(None)):
    """
    Verifica que la petición incluya en la URL el parámetro ?token=nivel-intermedio-2026
    Si no coincide o está ausente, retorna 401 Unauthorized.
    """
    if token != "nivel-intermedio-2026":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado: Token inválido o ausente"
        )
    return token
