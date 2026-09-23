# src/dominio/catalogo.py

CANCIONES = [
    {
        "id": "1",
        "titulo": "De Musica Ligera",
        "artista": "Soda Stereo",
        "album": "Cancion Animal",
        "genero": "Rock",
        "duracion_seg": "213",
    },
    {
        "id": "2",
        "titulo": "Persiana Americana",
        "artista": "Soda Stereo",
        "album": "Signos",
        "genero": "Rock",
        "duracion_seg": "263",
    },
    {
        "id": "3",
        "titulo": "Crimen",
        "artista": "Gustavo Cerati",
        "album": "Ahi vamos",
        "genero": "Rock",
        "duracion_seg": "239",
    },
]

import csv
import os


def versiones_de(id_cancion):
  resultado = []
  ruta = os.path.join("data", "versiones.txt")

  if not os.path.exists(ruta):
    return resultado

  try:
    with open(ruta, mode="r", encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        # Convertimos a string y quitamos espacios por seguridad
        cancion_id = row["cancion_id"].strip()
        version_de_id = row["version_de_id"].strip()

        # Comparamos como texto para evitar fallos de conversión
        if version_de_id == str(id_cancion):
          resultado.append(int(cancion_id))
          # Llamada recursiva
          resultado.extend(versiones_de(int(cancion_id)))
  except Exception:
    pass

  return resultado
