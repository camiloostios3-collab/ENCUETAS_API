from __future__ import annotations
from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from validators import DEPARTAMENTOS_COLOMBIA


class Encuestado(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Maria Garcia Lopez",
                "edad": 34,
                "estrato": 3,
                "departamento": "antioquia",
                "genero": "femenino",
                "nivel_educativo": "universitario",
                "ocupacion": "docente",
            }
        }
    )

    nombre: str = Field(..., min_length=2, max_length=100)
    edad: int = Field(..., ge=0, le=120)
    estrato: int = Field(..., ge=1, le=6)
    departamento: str = Field(...)
    genero: Optional[str] = Field(None)
    nivel_educativo: Optional[str] = Field(None)
    ocupacion: Optional[str] = Field(None, max_length=80)

    @field_validator("nombre", mode="before")
    @classmethod
    def normalizar_nombre(cls, v):
        if isinstance(v, str):
            return " ".join(v.strip().split()).title()
        return v

    @field_validator("departamento", mode="before")
    @classmethod
    def normalizar_departamento(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("departamento", mode="after")
    @classmethod
    def validar_departamento(cls, v: str) -> str:
        if v not in DEPARTAMENTOS_COLOMBIA:
            raise ValueError(
                f"'{v}' no es un departamento valido. "
                "Ejemplos: antioquia, cundinamarca, bogota d.c."
            )
        return v

    @field_validator("edad", mode="after")
    @classmethod
    def validar_edad(cls, v: int) -> int:
        if v < 0 or v > 120:
            raise ValueError(f"Edad debe estar entre 0 y 120. Recibido: {v}")
        return v

    @field_validator("estrato", mode="after")
    @classmethod
    def validar_estrato(cls, v: int) -> int:
        if v < 1 or v > 6:
            raise ValueError(f"Estrato debe estar entre 1 y 6. Recibido: {v}")
        return v


class RespuestaEncuesta(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id_pregunta": "P001",
                "tipo_pregunta": "likert",
                "valor": 4,
                "comentario": "De acuerdo.",
            }
        }
    )

    id_pregunta: str = Field(...)
    tipo_pregunta: str = Field(..., description="likert | porcentaje | abierta")
    valor: Union[int, float, str] = Field(...)
    comentario: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def validar_valor_segun_tipo(self) -> "RespuestaEncuesta":
        tipo = self.tipo_pregunta.lower()
        v = self.valor
        if tipo == "likert":
            if not isinstance(v, int) or v < 1 or v > 5:
                raise ValueError(f"Likert '{self.id_pregunta}': entero 1-5. Recibido: {v}")
        elif tipo == "porcentaje":
            if not isinstance(v, (int, float)) or not (0.0 <= float(v) <= 100.0):
                raise ValueError(f"Porcentaje '{self.id_pregunta}': valor 0.0-100.0. Recibido: {v}")
        elif tipo == "abierta":
            if not isinstance(v, str) or not v.strip():
                raise ValueError(f"Abierta '{self.id_pregunta}': texto no vacio requerido.")
        else:
            raise ValueError(f"Tipo desconocido: '{tipo}'. Usa: likert, porcentaje, abierta.")
        return self


class EncuestaCompleta(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "encuestado": {
                    "nombre": "Carlos Perez",
                    "edad": 28,
                    "estrato": 2,
                    "departamento": "cundinamarca",
                    "genero": "masculino",
                    "nivel_educativo": "tecnico",
                    "ocupacion": "conductor",
                },
                "respuestas": [
                    {"id_pregunta": "P001", "tipo_pregunta": "likert", "valor": 4, "comentario": None},
                    {"id_pregunta": "P002", "tipo_pregunta": "porcentaje", "valor": 75.5, "comentario": "Aprox"},
                    {"id_pregunta": "P003", "tipo_pregunta": "abierta", "valor": "Mejorar el transporte.", "comentario": None},
                ],
            }
        }
    )

    encuestado: Encuestado
    respuestas: List[RespuestaEncuesta] = Field(..., min_length=1)

    @field_validator("respuestas", mode="after")
    @classmethod
    def sin_preguntas_duplicadas(cls, v: List[RespuestaEncuesta]) -> List[RespuestaEncuesta]:
        ids = [r.id_pregunta for r in v]
        duplicados = {i for i in ids if ids.count(i) > 1}
        if duplicados:
            raise ValueError(f"IDs duplicados: {duplicados}")
        return v


class EncuestaAlmacenada(EncuestaCompleta):
    id: int


class Estadisticas(BaseModel):
    total_encuestas: int
    promedio_edad: float
    distribucion_por_estrato: dict[str, int]
    distribucion_por_departamento: dict[str, int]
    distribucion_por_genero: dict[str, int]
