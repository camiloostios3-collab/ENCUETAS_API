DEPARTAMENTOS_COLOMBIA = {
    "amazonas", "antioquia", "arauca", "atlantico", "bolivar", "boyaca",
    "caldas", "caqueta", "casanare", "cauca", "cesar", "choco", "cordoba",
    "cundinamarca", "guainia", "guaviare", "huila", "la guajira", "magdalena",
    "meta", "narino", "norte de santander", "putumayo", "quindio", "risaralda",
    "san andres", "santander", "sucre", "tolima", "valle del cauca",
    "vaupes", "vichada", "bogota d.c.",
}

TIPOS_PREGUNTA_VALIDOS = {"likert", "porcentaje", "abierta"}

def es_departamento_valido(departamento: str) -> bool:
    return departamento.strip().lower() in DEPARTAMENTOS_COLOMBIA

def es_tipo_pregunta_valido(tipo: str) -> bool:
    return tipo.strip().lower() in TIPOS_PREGUNTA_VALIDOS
