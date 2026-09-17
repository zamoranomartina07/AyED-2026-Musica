from src.config import TEMA
from src.dominio.biblioteca import Biblioteca

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
  print(
      f"{'ID':<4} | {'TÍTULO':<28} | {'ARTISTA':<25} | {'ÁLBUM':<22} |"
      f" {'GÉNERO':<10} | {'DURACIÓN'}"
  )
  print("-" * 110)
  for c in biblioteca.listar():
    print(
        f"{c.id:<4} | {c.titulo:<28} | {c.artista:<25} |"
        f" {c.album:<22} | {c.genero:<10} | {c.duracion_seg} s"
    )
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


def mostrar_menu():
  nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
  print()
  print(f"=== {nombre} — AyED C2 2026 ===")
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
    print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
    return

  biblioteca = Biblioteca()
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
    elif opcion in {"2", "3", "4", "6", "7", "8", "9"}:
      pendiente()
    else:
      print("Opción inválida.")


if __name__ == "__main__":
  main()
