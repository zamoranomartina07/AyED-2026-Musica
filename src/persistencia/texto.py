from pathlib import Path
from src.excepciones import ArchivoInvalidoError

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_TXT = DATA / "canciones.csv"


def cargar_texto(ruta):
    """Lee un archivo de texto y devuelve una lista de dicts, uno por registro."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")
    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip().split(",")
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            valores = linea.split(",")
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos "
                    f"(se esperaban {len(encabezado)}): {linea}"
                )
            filas.append(dict(zip(encabezado, valores)))
    return filas


def guardar_texto(ruta, filas, encabezados):
    """Escribe encabezado + un registro por línea."""
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            campos = [str(fila[clave]) for clave in encabezados]
            archivo.write(",".join(campos) + "\n")


# Nombres viejos del esqueleto, por si otro archivo los importa
cargar_csv = cargar_texto
guardar_csv = guardar_texto 
