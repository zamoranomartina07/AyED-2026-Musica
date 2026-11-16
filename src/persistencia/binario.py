"""Registros de longitud fija con struct para el dominio Música.

Header:
  magia     4s   b'AYED'
  tema      1s   b'M'
  cantidad  I    unsigned int (4 bytes)

Registro de Canción (105 bytes):
  id            I     unsigned int (4 bytes)
  titulo       30s    UTF-8 (30 bytes)
  artista      25s    UTF-8 (25 bytes)
  album        30s    UTF-8 (30 bytes)
  genero       12s    UTF-8 (12 bytes)
  anio          H     unsigned short (2 bytes)
  duracion_seg  H     unsigned short (2 bytes)
"""

import struct
from pathlib import Path
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError
from src.dominio.cancion import Cancion
from src.tads.lista_enlazada import ListaEnlazada

FORMATO = struct.Struct("<I 30s 25s 30s 12s 2H")  # id, titulo, artista, album, genero, anio, duracion_seg
HEADER = struct.Struct("<4s 1s I")  # magia, tema, cantidad

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_BIN = DATA / "canciones.bin"

TEMA = b"M" # Pokedex: P, Recetario: R, Musica: M

def _a_bytes(texto, ancho):
  """Texto → bytes UTF-8 de 'ancho' exacto: recorta o rellena con \\x00."""
  return texto.encode("utf-8")[:ancho].ljust(ancho, b"\x00")

def _a_texto(datos):
  """Bytes → texto: le saca los \\x00 del final."""
  return datos.rstrip(b"\x00").decode("utf-8")

def _item_a_tupla(p):
  """Objeto del dominio → tupla lista para FORMATO.pack"""
  return (
    int(p.id),
    _a_bytes(p.titulo, 20),
    _a_bytes(p.artista, 12),
    _a_bytes(p.album or "", 12),
    _a_bytes(p.genero, 12),
    int(p.anio),
    int(p.duracion_seg)
  )

def _tupla_a_item(t):
  """Tupla que salio de FORMATO.unpack → objeto del dominio"""
  return Cancion(
    id=t[0],
    titulo=_a_texto(t[1]),
    artista=_a_texto(t[2]),
    album=_a_texto(t[3]) or None,
    genero=_a_texto(t[4]),
    anio=t[5],
    duracion_seg=t[6]
  )


def guardar_binario(ruta, catalogo):
  """Escribe el archivo completo: header (magia + tema + cantidad) + registros."""
  with open(ruta, "wb") as archivo:
    archivo.write(HEADER.pack(b"AYED", TEMA, catalogo.tamanio()))
    for item in catalogo: # iterador de E3 otra vez
      archivo.write(FORMATO.pack(*_item_a_tupla(item)))


def cargar_binario(ruta):
  """Lee el binario con validaciones. Devuelve la ListaEnlazada de ítems."""
  with open(ruta, "rb") as archivo:
    cabecera = archivo.read(HEADER.size)
    if len(cabecera) < HEADER.size:
      raise ArchivoInvalidoError("Binario truncado: ni siquiera tiene header completo.")
    magia, tema, cantidad = HEADER.unpack(cabecera)
    if magia != b"AYED":
      raise ArchivoInvalidoError("Magia incorrecta: este archivo no es de este TP.")
    if tema != TEMA:
      raise ArchivoInvalidoError(f"El tema del archivo ({tema!r}) no es el mío ({TEMA!r}).")
    catalogo = ListaEnlazada()
    for _ in range(cantidad):
      datos = archivo.read(FORMATO.size)
      if len(datos) < FORMATO.size:
        raise ArchivoInvalidoError(
          "Binario truncado: el header dice más registros de los que hay."
      )
      catalogo.insertar_al_final(_tupla_a_item(FORMATO.unpack(datos)))
  return catalogo



def actualizar_registro(ruta, posicion, item):
  """Pisa SOLO el registro número 'posicion' (0-based) sin tocar el resto."""
  with open(ruta, "r+b") as archivo: # r+b = leer Y escribir
    archivo.seek(HEADER.size + posicion * FORMATO.size) # el salto del dibujo
    archivo.write(FORMATO.pack(*_item_a_tupla(item)))

def posicion_del_id(catalogo, id_buscado):
  """Devuelve la posición (0-based) del ítem con ese id, usando el iterador."""
  for posicion, item in enumerate(catalogo):
    if int(item.id) == int(id_buscado):
      return posicion
  raise ItemNoEncontradoError(f"No hay ítem con id {id_buscado}")

def alta_binario(ruta, item):
  """Agrega un registro AL FINAL y actualiza la cantidad del header."""
  with open(ruta, "r+b") as archivo:
    cabecera = archivo.read(HEADER.size)
    magia, tema, cantidad = HEADER.unpack(cabecera)
    archivo.seek(0, 2) # 2 = saltar al FINAL del archivo
    archivo.write(FORMATO.pack(*_item_a_tupla(item)))
    archivo.seek(0) # volver al principio
    archivo.write(HEADER.pack(magia, tema, cantidad + 1)) # arreglar cantidad

def baja_binario(ruta, posicion):
  """Quita el registro 'posicion': relee, saca ese registro y reescribe todo."""
  with open(ruta, "r+b") as archivo:
    cabecera = archivo.read(HEADER.size)
    magia, tema, cantidad = HEADER.unpack(cabecera)
    registros = [archivo.read(FORMATO.size) for _ in range(cantidad)]
    del registros[posicion] # afuera el dado de baja
    archivo.seek(0)
    archivo.truncate() # borra el contenido viejo
    archivo.write(HEADER.pack(magia, tema, len(registros)))
    for datos in registros:
      archivo.write(datos)
