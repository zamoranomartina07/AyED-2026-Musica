import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.tads.cola import Cola


class ColaReproduccion:
    """Cola de reproducción (FIFO)."""

    def __init__(self):
        self._cola = Cola()

    def encolar(self, cancion):
        self._cola.encolar(cancion)

    def siguiente(self):
        return self._cola.desencolar()

    def esta_vacia(self):
        return self._cola.esta_vacia()

    def __iter__(self):
        return iter(self._cola)