DEPARTAMENTOS_COLOMBIA = {
    "amazonas", "antioquia", "arauca",
    "atlantico", "atlántico",
    "bolivar", "bolívar",
    "boyaca", "boyacá",
    "caldas",
    "caqueta", "caquetá",
    "casanare", "cauca", "cesar",
    "choco", "chocó",
    "cordoba", "córdoba",
    "cundinamarca",
    "guainia", "guainía",
    "guaviare", "huila",
    "la guajira",
    "magdalena", "meta",
    "narino", "nariño",
    "norte de santander",
    "putumayo",
    "quindio", "quindío",
    "risaralda",
    "san andres", "san andrés",
    "santander", "sucre", "tolima",
    "valle del cauca",
    "vaupes", "vaupés",
    "vichada",
    "bogota d.c.", "bogotá d.c.",
}

TIPOS_PREGUNTA_VALIDOS = {"likert", "porcentaje", "abierta"}

def es_departamento_valido(departamento: str) -> bool:
    return departamento.strip().lower() in DEPARTAMENTOS_COLOMBIA

def es_tipo_pregunta_valido(tipo: str) -> bool:
    return tipo.strip().lower() in TIPOS_PREGUNTA_VALIDOS
