"""
Punto de entrada FastAPI + todos los endpoints.
RF3 - Endpoints REST.
RF4 - Manejador de errores 422.
RF5 - Endpoint async con explicacion.
RT5 - Decorador personalizado @log_request.
"""

import logging
import time
import functools
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models import EncuestaCompleta, EncuestaAlmacenada, Estadisticas

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Gestion de Encuestas Poblacionales",
    description="Sistema de recoleccion y validacion rigurosa de datos demograficos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db: dict[int, EncuestaAlmacenada] = {}
contador_id = 0


def log_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request") or next(
            (a for a in args if isinstance(a, Request)), None
        )
        inicio = time.perf_counter()
        resultado = await func(*args, **kwargs)
        duracion = (time.perf_counter() - inicio) * 1000
        if request:
            logger.info(
                "LOG %s | %s %s | %.2fms",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                request.method,
                request.url.path,
                duracion,
            )
        return resultado
    return wrapper


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        errores.append({
            "campo": " -> ".join(str(loc) for loc in error["loc"]),
            "mensaje": error["msg"],
            "tipo_error": error["type"],
            "valor_recibido": error.get("input"),
        })
    logger.warning("Ingesta invalida | ruta=%s | errores=%d", request.url.path, len(errores))
    return JSONResponse(
        status_code=422,
        content={
            "estado": "error_validacion",
            "mensaje": "Datos invalidos. Revise el detalle.",
            "total_errores": len(errores),
            "errores": errores,
        },
    )


@app.get("/")
async def root():
    return {"estado": "activo"}


@app.post("/encuestas/", response_model=EncuestaAlmacenada, status_code=201,
    summary="Registrar encuesta",
    description="Recibe y valida una encuesta completa. Retorna 201 con el ID asignado.")
async def crear_encuesta(encuesta: EncuestaCompleta, request: Request):
    global contador_id
    contador_id += 1
    nueva = EncuestaAlmacenada(id=contador_id, **encuesta.model_dump())
    db[contador_id] = nueva
    logger.info("Encuesta registrada ID=%d", contador_id)
    return nueva


@app.get("/encuestas/", response_model=List[EncuestaAlmacenada], status_code=200,
    summary="Listar encuestas",
    description="Retorna todas las encuestas almacenadas en memoria.")
@log_request
async def listar_encuestas(request: Request):
    return list(db.values())


@app.get("/encuestas/estadisticas/", response_model=Estadisticas, status_code=200,
    summary="Estadisticas generales",
    description="Total de encuestas, promedio de edad y distribuciones.")
async def obtener_estadisticas():
    if not db:
        return Estadisticas(
            total_encuestas=0, promedio_edad=0.0,
            distribucion_por_estrato={},
            distribucion_por_departamento={},
            distribucion_por_genero={},
        )
    encuestas = list(db.values())
    total = len(encuestas)
    promedio_edad = round(sum(e.encuestado.edad for e in encuestas) / total, 2)
    dist_estrato, dist_depto, dist_genero = {}, {}, {}
    for e in encuestas:
        k = f"estrato_{e.encuestado.estrato}"
        dist_estrato[k] = dist_estrato.get(k, 0) + 1
        d = e.encuestado.departamento
        dist_depto[d] = dist_depto.get(d, 0) + 1
        g = e.encuestado.genero or "no_especificado"
        dist_genero[g] = dist_genero.get(g, 0) + 1
    return Estadisticas(
        total_encuestas=total, promedio_edad=promedio_edad,
        distribucion_por_estrato=dist_estrato,
        distribucion_por_departamento=dist_depto,
        distribucion_por_genero=dist_genero,
    )


@app.get("/encuestas/{id}", response_model=EncuestaAlmacenada, status_code=200,
    summary="Obtener encuesta por ID",
    description="Retorna una encuesta por su ID. 404 si no existe.")
async def obtener_encuesta(id: int, request: Request):
    if id not in db:
        raise HTTPException(status_code=404, detail=f"Encuesta ID={id} no encontrada.")
    return db[id]


@app.put("/encuestas/{id}", response_model=EncuestaAlmacenada, status_code=200,
    summary="Actualizar encuesta",
    description="Reemplaza una encuesta existente. 404 si no existe.")
async def actualizar_encuesta(id: int, encuesta: EncuestaCompleta, request: Request):
    if id not in db:
        raise HTTPException(status_code=404, detail=f"Encuesta ID={id} no encontrada.")
    actualizada = EncuestaAlmacenada(id=id, **encuesta.model_dump())
    db[id] = actualizada
    logger.info("Encuesta ID=%d actualizada.", id)
    return actualizada


@app.delete("/encuestas/{id}", status_code=204,
    summary="Eliminar encuesta",
    description="Elimina una encuesta por ID. 204 sin contenido. 404 si no existe.")
async def eliminar_encuesta(id: int, request: Request):
    if id not in db:
        raise HTTPException(status_code=404, detail=f"Encuesta ID={id} no encontrada.")
    del db[id]
    logger.info("Encuesta ID=%d eliminada.", id)
