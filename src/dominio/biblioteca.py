import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

#from src.dominio.cancion import Cancion
#from src.dominio.catalogo import CANCIONES  #ya no se usan porque ahora se cargan desde el archivo de texto/CSV
from src.tads.lista_enlazada import ListaEnlazada
from src.persistencia.texto import armar_catalogo_desde_txt, RUTA_CANCIONES


class Biblioteca:
    def __init__(self):
        self._canciones = ListaEnlazada()
        self.versiones = {}  # id_version -> (id_original, tipo)
        self._cargar_canciones()
        self._cargar_versiones()

    def _cargar_canciones(self):
        """Carga las canciones desde el archivo de texto/CSV al iniciar."""
        try:
            self._canciones = armar_catalogo_desde_txt(RUTA_CANCIONES)
        except Exception:
            # Por si el archivo no existe al arrancar por primera vez
            pass

    def _cargar_versiones(self):
        ruta = os.path.join("data", "versiones.csv")
        try:
            with open(ruta, encoding="utf-8") as f:
                next(f, None)  # Saltar encabezado
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
            if int(c.id) == int(id_cancion):
                return c
        return None

    def versiones_directas(self, id_cancion):
        directas = []
        for id_v, (id_orig, tipo) in self.versiones.items():
            if int(id_orig) == int(id_cancion):
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

    def generar_siguiente_id(self):
        """Calcula el próximo ID disponible (máximo ID actual + 1)."""
        if self._canciones.tamanio() == 0:
            return 1
        max_id = max(int(c.id) for c in self._canciones)
        return max_id + 1

    def actualizar_canciones(self, nueva_lista):
            """Reemplaza la lista enlazada interna con una nueva colección ordenada."""
            nueva_enlazada = ListaEnlazada()
            for cancion in nueva_lista:
                nueva_enlazada.insertar_al_final(cancion) # <-- Aquí usamos el método correcto de tu TDA
            self._canciones = nueva_enlazada