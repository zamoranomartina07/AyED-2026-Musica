import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.tads.nodo import Nodo


class ListaEnlazada:
    """TAD lista enlazada simple. No usar list de Python por abajo."""

    def __init__(self):
        self._cabeza = None
        self._tamanio = 0

    def esta_vacia(self):
        return self._cabeza is None

    def tamanio(self):
        return self._tamanio

    def insertar_al_inicio(self, dato):
        self._cabeza = Nodo(dato, self._cabeza)
        self._tamanio += 1

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
            self._tamanio += 1
            return

        actual = self._cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo
        self._tamanio += 1

    def insertar_ordenado(self, dato, clave):
        """Inserta manteniendo orden ascendente según clave(dato)."""
        valor = clave(dato)
        if self._cabeza is None or valor < clave(self._cabeza.dato):
            self.insertar_al_inicio(dato)
            return

        actual = self._cabeza
        while actual.siguiente is not None and clave(actual.siguiente.dato) <= valor:
            actual = actual.siguiente
        actual.siguiente = Nodo(dato, actual.siguiente)
        self._tamanio += 1

    def eliminar(self, dato):
        if self._cabeza is None:
            return

        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._tamanio -= 1
            return

        actual = self._cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self._tamanio -= 1
                return
            actual = actual.siguiente

    def buscar(self, dato):
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return actual
            actual = actual.siguiente
        return None

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

