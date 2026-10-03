from src.tads.pila import Pila


class Historial:
    """Historial de reproducción con deshacer (pila)."""

        def __init__(self):
                self._pila = Pila()

                    def registrar(self, cancion):
                            self._pila.apilar(cancion)

                                def deshacer(self):
                                        return self._pila.desapilar()

                                            def esta_vacio(self):
                                                    return self._pila.esta_vacia()

                                                        def __iter__(self):
                                                                return iter(self._pila)