def busqueda_lineal(coleccion, clave, obtener_clave):
    """Devuelve el ítem cuya clave coincide, o None si no existe."""
    for elemento in coleccion:
        if obtener_clave is None:
            if elemento == clave:
                return elemento
        elif obtener_clave(elemento) == clave:
            return elemento
    return None



def busqueda_binaria(coleccion_ordenada, clave, obtener_clave):
    """La colección tiene que estar ordenada por obtener_clave."""
    izquierda = 0
    derecha = len(coleccion_ordenada) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        elemento_medio = coleccion_ordenada[medio]
        clave_medio = obtener_clave(elemento_medio)
        if clave_medio == clave:
            return elemento_medio
        elif clave_medio < clave:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return None
