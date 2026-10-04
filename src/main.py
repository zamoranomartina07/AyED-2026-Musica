import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import TEMA
from src.dominio.biblioteca import Biblioteca
from src.dominio.playlist import Playlist
from src.dominio.historial import Historial
from src.dominio.cola_reproduccion import ColaReproduccion
from src.excepciones import (
    ColeccionLlenaError,
        PilaVaciaError,
            ColaVaciaError,
                ItemNoEncontradoError,
                )

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def listar_catalogo(biblioteca):
    print("\n" + "=" * 110)
    print(" " * 40 + "CATÁLOGO DE LA BIBLIOTECA MUSICAL")
    print("=" * 110)
    print(f"{'ID':<4} | {'TÍTULO':<28} | {'ARTISTA':<25} | {'ÁLBUM':<22} | {'GÉNERO':<10} | {'DURACIÓN'}")
    print("-" * 110)
    for c in biblioteca.listar():
        print(f"{c.id:<4} | {c.titulo:<28} | {c.artista:<25} | {c.album:<22} | {c.genero:<10} | {c.duracion_seg} s")
    print("=" * 110)


def mostrar_versiones(biblioteca):
    id_cancion = input("ID de la canción: ").strip()
    cancion = biblioteca.buscar(id_cancion)
    if cancion is None:
        print("No existe esa canción.")
        return

    ids_versiones = biblioteca.versiones_de(id_cancion)
    if not ids_versiones:
        print(f"'{cancion.titulo}' no tiene versiones registradas.")
        return

    print(f"Versiones derivadas de '{cancion.titulo}':")
    for id_v in ids_versiones:
        v = biblioteca.buscar(id_v)
        print(f" - {v.titulo} ({v.artista})")


def pedir_cancion(biblioteca):
    id_cancion = input("ID de la canción: ").strip()
    cancion = biblioteca.buscar(id_cancion)
    if cancion is None:
        print("❌ No existe esa canción.")
    return cancion


def menu_playlist(biblioteca, playlist):
    while True:
        print("\n--- Playlist ---")
        print("1. Agregar canción")
        print("2. Quitar canción")
        print("3. Listar playlist")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            cancion = pedir_cancion(biblioteca)
            if cancion is not None:
                try:
                    playlist.agregar(cancion)
                    print(f"✅ Agregada: {cancion.resumen()}")
                except ColeccionLlenaError as e:
                    print(f"❌ {e}")
        elif opcion == "2":
            cancion = pedir_cancion(biblioteca)
            if cancion is not None:
                try:
                    playlist.quitar(cancion)
                    print(f"✅ Quitada: {cancion.resumen()}")
                except ItemNoEncontradoError as e:
                    print(f"❌ {e}")
        elif opcion == "3":
            print(f"Playlist ({playlist.tamanio()}/{playlist.tope()}):")
            for c in playlist:
                print(f" - {c}")
        else:
            print("Opción inválida.")


def menu_historial(historial):
    while True:
        print("\n--- Historial de reproducción ---")
        print("1. Ver historial")
        print("2. Deshacer última reproducción")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            for c in historial:
                print(f" - {c}")
        elif opcion == "2":
            try:
                c = historial.deshacer()
                print(f"↩ Deshecho: {c}")
            except PilaVaciaError as e:
                print(f"❌ {e}")
        else:
            print("Opción inválida.")


def menu_cola(biblioteca, cola, historial):
    while True:
        print("\n--- Cola de reproducción ---")
        print("1. Encolar canción")
        print("2. Reproducir siguiente")
        print("3. Ver cola")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            cancion = pedir_cancion(biblioteca)
            if cancion is not None:
                cola.encolar(cancion)
                print(f"✅ Encolada: {cancion.resumen()}")
        elif opcion == "2":
            try:
                c = cola.siguiente()
                historial.registrar(c)
                print(f"▶ Sonando: {c}")
            except ColaVaciaError as e:
                print(f"❌ {e}")
        elif opcion == "3":
            for c in cola:
                print(f" - {c}")
        else:
            print("Opción inválida.")


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA) or "(sin tema)"
    print()
    print(f"=== {nombre} · AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva (versiones de una canción)")
    print("6. Colección principal (equipo / menú / playlist)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")


def main():
    if TEMA not in TEMAS:
        print("Setear TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    biblioteca = Biblioteca()
    playlist = Playlist()
    historial = Historial()
    cola = ColaReproduccion()

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()

        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(biblioteca)
        elif opcion == "5":
            mostrar_versiones(biblioteca)
        elif opcion == "6":
            menu_playlist(biblioteca, playlist)
        elif opcion == "7":
            menu_historial(historial)
        elif opcion == "8":
            menu_cola(biblioteca, cola, historial)
        elif opcion in {"2", "3", "4", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
