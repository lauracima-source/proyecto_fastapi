import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db_usuarios, db_productos  # Importación requerida por la consigna

client = TestClient(app)

# ==========================================
# Ejercicio 1: Pruebas sobre Componente Usuarios
# ==========================================

def test_1_1_registro_exitoso():
    """Validar que enviar un usuario válido devuelva un código 201 Created."""
    usuario_valido = {
        "id": 10,
        "username": "juan_perez",
        "edad": 20
    }
    response = client.post("/usuarios/", json=usuario_valido)
    assert response.status_code == 201
    assert response.json()["username"] == "juan_perez"


def test_1_2_fallo_validacion_esquema():
    """Comprobar que un usuario con edad menor a 18 devuelva 422 Unprocessable Entity."""
    usuario_menor = {
        "id": 11,
        "username": "maria_gomez",
        "edad": 16  # Edad menor a 18 (Inválido)
    }
    response = client.post("/usuarios/", json=usuario_menor)
    assert response.status_code == 422


def test_1_3_control_de_duplicados():
    """Validar que intentar registrar un usuario o ID existente responda 400 Bad Request."""
    usuario_duplicado = {
        "id": 10,  # Ya registrado en el test 1.1
        "username": "juan_perez",
        "edad": 25
    }
    response = client.post("/usuarios/", json=usuario_duplicado)
    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario o ID ya existe en la base de datos."


def test_1_4_busqueda_por_id_y_parametros():
    """
    Validar:
    1. Búsqueda por ID existente devuelve 200 OK y el campo 'buscar' toma 'general' por defecto.
    2. Si el ID no existe, devuelve 404 Not Found.
    3. Si el Path parameter es inválido (<= 0), devuelve 422 Unprocessable Entity.
    """
    # Case 1: ID existente (id=10)
    res_ok = client.get("/usuarios/10")
    assert res_ok.status_code == 200
    assert res_ok.json()["buscar"] == "general"

    # Case 1b: Probando enviar un Query Parameter personalizado
    res_query = client.get("/usuarios/10?buscar=filtro_custom")
    assert res_query.status_code == 200
    assert res_query.json()["buscar"] == "filtro_custom"

    # Case 2: ID inexistente
    res_not_found = client.get("/usuarios/9999")
    assert res_not_found.status_code == 404

    # Case 3: Path Parameter inválido (user_id = 0)
    res_invalido = client.get("/usuarios/0")
    assert res_invalido.status_code == 422


# ==========================================
# Ejercicio 2: Pruebas sobre Seguridad e Inyección Local
# ==========================================

def test_2_1_acceso_concedido_token_correcto():
    """Enviar POST con ?token=nivel-intermedio-2026 y verificar retorno 201 Created."""
    item_nuevo = {
        "id": 100,
        "nombre": "Teclado Gamer",
        "precio": 120.50
    }
    response = client.post("/productos/?token=nivel-intermedio-2026", json=item_nuevo)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Teclado Gamer"


def test_2_2_acceso_denegado_token_incorrecto():
    """Enviar POST con token erróneo o ausente y comprobar código 401 Unauthorized."""
    item_nuevo = {
        "id": 101,
        "nombre": "Mouse Óptico",
        "precio": 30.00
    }
    # Caso 1: Token erróneo
    res_malo = client.post("/productos/?token=token-incorrecto", json=item_nuevo)
    assert res_malo.status_code == 401

    # Caso 2: Token ausente
    res_ausente = client.post("/productos/", json=item_nuevo)
    assert res_ausente.status_code == 401


# ==========================================
# Ejercicio 3: Pruebas de Bloqueo Perimetral Global
# ==========================================

def test_3_1_proteccion_por_enrutador():
    """
    Realizar un GET a /productos/ (listar productos) sin token.
    Aunque el endpoint handler no tiene 'Depends' explícito en su función,
    el router entero está protegido desde main.py. Debe devolver 401 Unauthorized.
    """
    response = client.get("/productos/")
    assert response.status_code == 401