import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

encuesta_valida = {
    "encuestado": {
        "nombre": "Maria Lopez",
        "edad": 30,
        "estrato": 3,
        "departamento": "antioquia",
        "genero": "femenino",
        "nivel_educativo": "universitario",
        "ocupacion": "docente"
    },
    "respuestas": [
        {"id_pregunta": "P01", "tipo_pregunta": "likert",     "valor": 4,    "comentario": None},
        {"id_pregunta": "P02", "tipo_pregunta": "likert",     "valor": 3,    "comentario": None},
        {"id_pregunta": "P03", "tipo_pregunta": "porcentaje", "valor": 30.0, "comentario": None},
        {"id_pregunta": "P04", "tipo_pregunta": "porcentaje", "valor": 4,    "comentario": None},
        {"id_pregunta": "P05", "tipo_pregunta": "abierta",    "valor": "Falta de empleo", "comentario": None}
    ]
}


def test_crear_encuesta():
    r = client.post("/encuestas/", json=encuesta_valida)
    assert r.status_code == 201
    assert "id" in r.json()


def test_listar_encuestas():
    r = client.get("/encuestas/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_obtener_encuesta_existente():
    r = client.post("/encuestas/", json=encuesta_valida)
    id_ = r.json()["id"]
    r2 = client.get(f"/encuestas/{id_}")
    assert r2.status_code == 200


def test_obtener_encuesta_inexistente():
    r = client.get("/encuestas/9999")
    assert r.status_code == 404


def test_eliminar_encuesta():
    r = client.post("/encuestas/", json=encuesta_valida)
    id_ = r.json()["id"]
    r2 = client.delete(f"/encuestas/{id_}")
    assert r2.status_code == 204


def test_error_422_datos_invalidos():
    r = client.post("/encuestas/", json={"encuestado": {"nombre": "X", "edad": 200}, "respuestas": []})
    assert r.status_code == 422
    assert r.json()["estado"] == "error_validacion"


def test_estadisticas():
    r = client.get("/encuestas/estadisticas/")
    assert r.status_code == 200
