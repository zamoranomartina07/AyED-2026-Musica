from pathlib import Path
from src.excepciones import ArchivoInvalidoError
from src.tads.lista_enlazada import ListaEnlazada
from src.dominio.cancion import Cancion

# RAIZ = la carpeta del repo (donde está README.md).
# texto.py está en src/persistencia/, así que subimos 3 niveles:
# parents[0]=persistencia parents[1]=src parents[2]=repo
RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_CANCIONES = DATA / "canciones.csv"

def cargar_texto(ruta):
    """Lee un .txt (o .csv) secuencial y devuelve una LISTA DE DICTS, uno por registro.
    La primera línea es el encabezado; cada línea siguiente es un registro
    con campos separados por coma. Si el archivo no existe o una línea
    tiene más/menos campos que el encabezado, lanza ArchivoInvalidoError.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")

    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip().split(",")
        for linea in archivo:
            linea = linea.strip()
            if not linea: # línea vacía al final del archivo
                continue
            valores = linea.split(",")
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos "
                    f"(se esperaban {len(encabezado)}): {linea}"
                )
            fila = dict(zip(encabezado, valores)) # {'id': '1', 'nombre': ...}
            filas.append(fila)
    return filas

def armar_catalogo_desde_txt(ruta):
    """Lee el .txt y devuelve la ListaEnlazada con objetos del dominio."""
    catalogo = ListaEnlazada()
    for fila in cargar_texto(ruta):
        cancion = Cancion(
            id=int(fila["id"]), # acá se convierten los números
            titulo=fila["titulo"],
            artista=fila["artista"],
            album=fila["album"] or None, # si viene vacío → None
            genero=fila["genero"],
            anio=int(fila["anio"]),
            duracion_seg=int(fila["duracion_seg"]),
        )
        catalogo.insertar_al_final(cancion)
    return catalogo

def armar_versiones_desde_txt(ruta):
    """Devuelve un dict {origen_id: [destino_id, ...]} para la recursión de E2."""
    versiones = {}
    for fila in cargar_texto(ruta):
        origen = int(fila["cancion_id"])
        destino = int(fila["version_de_id"])
        if origen not in versiones:
            versiones[origen] = []
        versiones[origen].append(destino)
    return versiones

def guardar_texto(ruta, filas, encabezados):
    """Escribe el catálogo en .txt: encabezado + un registro por línea.
    filas: iterable de dicts. encabezados: lista con el orden de las columnas."""
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            valores = [str(fila[header]) for header in encabezados]
            archivo.write(",".join(valores) + "\n")
