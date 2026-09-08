from src.config import TEMA

import csv
import os
from src.config import TEMA

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def cargar_y_listar_catalogo():
    # Ruta hacia el dataset de canciones dentro de esqueleto/data/
    ruta_csv = os.path.join("esqueleto", "data", "canciones.csv")

    if not os.path.exists(ruta_csv):
        # Ruta alternativa si ejecutas desde la carpeta esqueleto
        ruta_csv = os.path.join("data", "canciones.csv")

    if not os.path.exists(ruta_csv):
        print(f"\n[Error] No se encontró el archivo de datos en {ruta_csv}")
        return

    print("\n" + "=" * 110)
    print(" " * 40 + "CATÁLOGO DE LA BIBLIOTECA MUSICAL")
    print("=" * 110)
    print(f"{'ID':<4} | {'TÍTULO':<28} | {'ARTISTA':<25} | {'ÁLBUM':<22} | {'GÉNERO':<10} | {'DURACIÓN'}")
    print("-" * 110)

    with open(ruta_csv, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for c in lector:
            print(f"{c['id']:<4} | {c['titulo']:<28} | {c['artista']:<25} | {c['album']:<22} | {c['genero']:<10} | {c['duracion_seg']}s")
    print("=" * 110)


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (equipo / menú / playlist)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")


def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            cargar_y_listar_catalogo()
        elif opcion in {"2", "3", "4", "5", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
