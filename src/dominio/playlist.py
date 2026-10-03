from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError, ItemNoEncontradoError


class Playlist:
    """Colección principal con tope, sobre ListaEnlazada."""

        def __init__(self, tope=5):
                self._canciones = ListaEnlazada()
                        self._tope = tope

                            def agregar(self, cancion):
                                    if self._canciones.tamanio() >= self._tope:
                                                raise ColeccionLlenaError(
                                                                f"La playlist está llena (máximo {self._tope})."
                                                                            )
                                                                                    self._canciones.insertar_al_final(cancion)

                                                                                        def quitar(self, cancion):
                                                                                                if self._canciones.buscar(cancion) is None:
                                                                                                            raise ItemNoEncontradoError("Esa canción no está en la playlist.")
                                                                                                                    self._canciones.eliminar(cancion)

                                                                                                                        def tope(self):
                                                                                                                                return self._tope

                                                                                                                                    def tamanio(self):
                                                                                                                                            return self._canciones.tamanio()

                                                                                                                                                def esta_vacia(self):
                                                                                                                                                        return self._canciones.esta_vacia()

                                                                                                                                                            def __iter__(self):
                                                                                                                                                                    return iter(self._canciones)