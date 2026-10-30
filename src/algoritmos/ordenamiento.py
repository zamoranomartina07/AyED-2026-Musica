def ordenar_seleccion(coleccion, clave):
    """Ordenamiento por selección. Devuelve una nueva secuencia, no usa sorted."""
    a = list(coleccion)
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if clave(a[j]) < clave(a[m]):
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def ordenar_insercion(coleccion, clave):
    """Ordenamiento por inserción. Devuelve una nueva secuencia, no usa sorted."""
    a = list(coleccion)
    for i in range(1, len(a)):
        actual = a[i]
        j = i - 1
        while j >= 0 and clave(a[j]) > clave(actual):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a
