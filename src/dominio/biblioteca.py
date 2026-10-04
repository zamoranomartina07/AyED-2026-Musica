import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.dominio.cancion import Cancion
from src.dominio.catalogo import CANCIONES
from src.tads.lista_enlazada import ListaEnlazada


class Biblioteca:
    def __init__(self):
        self._canciones = ListaEnlazada()
        self.versiones = {}  # id_version -> (id_original, tipo)
        self._cargar_canciones()
        self._cargar_versiones()

    def _cargar_canciones(self):
        for c in CANCIONES:
            self._canciones.insertar_al_final(Cancion(**c))

    def _cargar_versiones(self):
        ruta = os.path.join("data", "versiones.txt")
        try:
            with open(ruta, encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    id_version, id_original, tipo = linea.split(",")
                    self.versiones[id_version] = (id_original, tipo)
        except FileNotFoundError:
            pass

    def listar(self):
        return self._canciones

    def tamanio(self):
        return self._canciones.tamanio()

    def __iter__(self):
        return iter(self._canciones)

    def buscar(self, id_cancion):
        for c in self._canciones:
            if c.id == str(id_cancion):
                return c
        return None

    def versiones_directas(self, id_cancion):
        directas = []
        for id_v, (id_orig, tipo) in self.versiones.items():
            if id_orig == str(id_cancion):
                directas.append(id_v)
        return directas

    def versiones_de(self, id_cancion):
        """Lista todas las versiones derivadas de una cancion (directas e indirectas)."""
        directas = self.versiones_directas(id_cancion)
        if not directas:  # CASO BASE
            return []
        resultado = list(directas)
        for v in directas:  # CASO RECURSIVO
            resultado += self.versiones_de(v)
        return resultado
