# API de Gestion de Encuestas Poblacionales

API REST construida con FastAPI para recolectar y validar datos de encuestas demograficas colombianas.

## Tecnologias
- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn

## Instalacion

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd encuesta-api
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Ejecucion
```bash
uvicorn main:app --reload
```

La API estara disponible en: http://127.0.0.1:8000

## Documentacion
- Swagger UI: http://127.0.0.1:8000/docs
- Redoc:      http://127.0.0.1:8000/redoc

## Endpoints
| Verbo  | Ruta                      | Descripcion                  |
|--------|---------------------------|------------------------------|
| POST   | /encuestas/               | Registrar encuesta           |
| GET    | /encuestas/               | Listar encuestas             |
| GET    | /encuestas/{id}           | Obtener encuesta por ID      |
| PUT    | /encuestas/{id}           | Actualizar encuesta          |
| DELETE | /encuestas/{id}           | Eliminar encuesta            |
| GET    | /encuestas/estadisticas/  | Estadisticas generales       |

## Entorno virtual: venv vs conda
Se uso **venv** porque es nativo de Python, no requiere instalacion adicional
y es suficiente para proyectos con dependencias simples como este.
Conda es preferible cuando se necesitan paquetes no-Python (C, R, CUDA, etc.).
