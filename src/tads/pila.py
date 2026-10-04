import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.excepciones import PilaVaciaError
from src.tads.lista_enlazada import ListaEnlazada


class Pila:
    """TAD pila implementado sobre ListaEnlazada."""

    def __init__(self):
        self._items = ListaEnlazada()

    def apilar(self, dato):
        self._items.insertar_al_inicio(dato)

    def desapilar(self):
        if self.esta_vacia():
            raise PilaVaciaError("No hay elementos en el historial para deshacer.")
        tope = self.ver_tope()
        self._items.eliminar(tope)
        return tope

    def ver_tope(self):
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía.")
        for dato in self._items:
            return dato

    def esta_vacia(self):
        return self._items.esta_vacia()

    def tamanio(self):
        return self._items.tamanio()

    def __iter__(self):
        return iter(self._items)
