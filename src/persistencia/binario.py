"""Registros de longitud fija con struct.

Layout sugerido (documentar el definitivo en docs/INFORME.md):

Header:
  magia     4s   b'AYED'
  tema      1s   b'P' | b'R' | b'M'
  cantidad  I    unsigned int

El registro depende del tema. Ejemplo Pokédex:
  id          I
  nombre     20s
  tipo1      12s
  tipo2      12s
  hp          H
  ataque      H
  defensa     H
  velocidad   H
  generacion  H
"""


import struct
from src.excepciones import ArchivoInvalidoError

MAGIC_HEADER = b'AYED'
TEMA_CARACTER = b'M'  # 'M' de Música
# Formato del registro: id(I), titulo(30s), artista(30s), duracion(f)
FORMATO_REGISTRO = "=I30s30sf"
TAMANO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)
TAMANO_HEADER = struct.calcsize("=4scI")


def guardar_binario(ruta, items):
    """Guarda el catálogo (lista de dicts) en un archivo binario con header y registros de tamaño fijo."""
    try:
        with open(ruta, "wb") as f:
            cantidad = len(items)
            header = struct.pack("=4scI", MAGIC_HEADER, TEMA_CARACTER, cantidad)
            f.write(header)
            
            for item in items:
                # Extraemos y casteamos los datos del diccionario
                id_val = int(item["id"])
                titulo_str = str(item["titulo"])
                artista_str = str(item["artista"])
                duracion_val = float(item["duracion_seg"])

                # Asegurar tamaño fijo de 30 bytes para strings codificados en utf-8
                titulo_bytes = titulo_str.encode("utf-8")[:30].ljust(30, b"\x00")
                artista_bytes = artista_str.encode("utf-8")[:30].ljust(30, b"\x00")
                
                registro = struct.pack(FORMATO_REGISTRO, id_val, titulo_bytes, artista_bytes, duracion_val)
                f.write(registro)
    except IOError as e:
        raise ArchivoInvalidoError(f"No se pudo escribir el archivo binario: {e}")


def cargar_binario(ruta):
    """Carga los registros desde el archivo binario validando el header y la firma."""
    items = []
    try:
        with open(ruta, "rb") as f:
            header_bytes = f.read(TAMANO_HEADER)
            if len(header_bytes) < TAMANO_HEADER:
                raise ArchivoInvalidoError("Archivo binario incompleto o corrupto en el header.")
            
            magia, tema, cantidad = struct.unpack("=4scI", header_bytes)
            
            if magia != MAGIC_HEADER:
                raise ArchivoInvalidoError("Firma mágica inválida en el archivo binario.")
            
            for _ in range(cantidad):
                bloque = f.read(TAMANO_REGISTRO)
                if len(bloque) < TAMANO_REGISTRO:
                    raise ArchivoInvalidoError("Archivo binario truncado: faltan registros.")
                
                id_val, titulo_bytes, artista_bytes, duracion_val = struct.unpack(FORMATO_REGISTRO, bloque)
                
                titulo = titulo_bytes.rstrip(b"\x00").decode("utf-8", errors="ignore")
                artista = artista_bytes.rstrip(b"\x00").decode("utf-8", errors="ignore")
                
                # Reconstruimos el diccionario con el formato original del dominio
                items.append({
                    "id": str(id_val),
                    "titulo": titulo,
                    "artista": artista,
                    "album": "",  # Campo por defecto si el struct guardaba lo básico
                    "genero": "", # Campo por defecto
                    "duracion_seg": str(int(duracion_val))
                })
        return items
    except FileNotFoundError:
        return []
    except Exception as e:
        if isinstance(e, ArchivoInvalidoError):
            raise e
        raise ArchivoInvalidoError(f"Error al leer el archivo binario: {e}")


def actualizar_registro(ruta, posicion, item):
    """Pisa un registro por posición (acceso directo). posicion es 0-based."""
    try:
        with open(ruta, "r+b") as f:
            header_bytes = f.read(TAMANO_HEADER)
            if len(header_bytes) < TAMANO_HEADER or header_bytes[:4] != MAGIC_HEADER:
                raise ArchivoInvalidoError("Archivo binario inválido para actualización.")
            
            # Calcular la posición exacta saltando el header + desplazamiento por índice
            desplazamiento = TAMANO_HEADER + (posicion * TAMANO_REGISTRO)
            
            f.seek(0, 2)
            tamanio_total = f.tell()
            if desplazamiento + TAMANO_REGISTRO > tamanio_total:
                raise ArchivoInvalidoError("La posición indicada está fuera de los límites del archivo.")
            
            f.seek(desplazamiento)
            
            id_val = int(item["id"])
            titulo_str = str(item["titulo"])
            artista_str = str(item["artista"])
            duracion_val = float(item["duracion_seg"])

            titulo_bytes = titulo_str.encode("utf-8")[:30].ljust(30, b"\x00")
            artista_bytes = artista_str.encode("utf-8")[:30].ljust(30, b"\x00")
            
            registro = struct.pack(FORMATO_REGISTRO, id_val, titulo_bytes, artista_bytes, duracion_val)
            f.write(registro)
    except IOError as e:
        raise ArchivoInvalidoError(f"Error de E/S al actualizar el registro por posición: {e}")