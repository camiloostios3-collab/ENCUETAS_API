import pytest
from pydantic import ValidationError
from models import Encuestado, RespuestaEncuesta, EncuestaCompleta


def test_encuestado_valido():
    e = Encuestado(nombre="Carlos Perez", edad=28, estrato=2, departamento="cundinamarca")
    assert e.nombre == "Carlos Perez"


def test_edad_invalida():
    with pytest.raises(ValidationError):
        Encuestado(nombre="Ana", edad=150, estrato=1, departamento="antioquia")


def test_estrato_invalido():
    with pytest.raises(ValidationError):
        Encuestado(nombre="Luis", edad=30, estrato=9, departamento="antioquia")


def test_departamento_invalido():
    with pytest.raises(ValidationError):
        Encuestado(nombre="Juan", edad=25, estrato=3, departamento="narnia")


def test_respuesta_likert_valida():
    r = RespuestaEncuesta(id_pregunta="P001", tipo_pregunta="likert", valor=3)
    assert r.valor == 3


def test_respuesta_likert_invalida():
    with pytest.raises(ValidationError):
        RespuestaEncuesta(id_pregunta="P001", tipo_pregunta="likert", valor=9)


def test_respuesta_porcentaje_invalida():
    with pytest.raises(ValidationError):
        RespuestaEncuesta(id_pregunta="P002", tipo_pregunta="porcentaje", valor=150.0)


def test_ids_duplicados():
    with pytest.raises(ValidationError):
        EncuestaCompleta(
            encuestado=Encuestado(nombre="Ana Torres", edad=22, estrato=1, departamento="antioquia"),
            respuestas=[
                RespuestaEncuesta(id_pregunta="P001", tipo_pregunta="likert", valor=4),
                RespuestaEncuesta(id_pregunta="P001", tipo_pregunta="likert", valor=2),
            ]
        )
