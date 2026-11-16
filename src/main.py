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
    ArchivoInvalidoError
                )
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion
from src.persistencia.texto import (
    RUTA_CANCIONES,
    guardar_texto,
    armar_catalogo_desde_txt,
)
from src.persistencia.binario import (
    guardar_binario, 
    cargar_binario,
    alta_binario,
    baja_binario,
    actualizar_registro,
    posicion_del_id,
    RUTA_BIN,
    )

from src.dominio.cancion import Cancion

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}
ENCABEZADOS = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]


"""Menu principal de la aplicación, con submenús para cada funcionalidad."""
def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA) or "(sin tema)"
    print()
    print(f"=== {nombre} · AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. versiones de una canción")
    print("6. Modificar colecciones (playlist / catálogo)")
    print("7. Historial (pila)")
    print("8. Cola de reproducción")
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
        elif opcion == "2":
            mostrar_detalle(biblioteca)    
        elif opcion == "3":
            menu_busqueda(biblioteca)      
        elif opcion == "4":
            menu_ordenamiento(biblioteca)
        elif opcion == "5":
            mostrar_versiones(biblioteca)
        elif opcion == "6":
            menu_colecciones(biblioteca, playlist)
        elif opcion == "7":
            menu_historial(historial)
        elif opcion == "8":
            menu_cola(biblioteca, cola, historial)
        elif opcion == "9":
            menu_guardar_cargar(biblioteca)
        else:
            print("Opción inválida.")

def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")

def pedir_cancion(biblioteca):
    id_cancion = input("ID de la canción: ").strip()
    cancion = biblioteca.buscar(id_cancion)
    if cancion is None:
        print("❌ No existe esa canción.")
    return cancion

def filas_del_catalogo(catalogo):
    """Convierte los objetos del dominio en dicts para guardar_texto."""
    filas = []
    for p in catalogo: 
        filas.append({
            "id": p.id,
            "titulo": p.titulo,
            "artista": p.artista,
            "album": p.album,
            "genero": p.genero or "",
            "anio": p.anio,
            "duracion_seg": p.duracion_seg,
            })
    return filas

def guardar_todo(catalogo):
    """Guarda el catálogo en .txt y .bin, sobrescribiendo ambos archivos."""
    guardar_texto(RUTA_CANCIONES, filas_del_catalogo(catalogo), ENCABEZADOS)
    guardar_binario(RUTA_CANCIONES.with_suffix(".bin"), catalogo)
    print("✅ Catálogo guardado en .txt y .bin.")


"""1. FUNCIONES DE LISTADO"""
def listar_catalogo(biblioteca):
    print("\n" + "=" * 110)
    print(" " * 40 + "CATÁLOGO DE LA BIBLIOTECA MUSICAL")
    print("=" * 110)
    print(f"{'ID':<4} | {'TÍTULO':<28} | {'ARTISTA':<25} | {'ÁLBUM':<22} | {'GÉNERO':<10} | {'DURACIÓN'}")
    print("-" * 110)
    for c in biblioteca.listar():
        print(f"{c.id:<4} | {c.titulo:<28} | {c.artista:<25} | {c.album:<22} | {c.genero:<10} | {c.duracion_seg} s")
    print("=" * 110)


"""2. MENU DE DETALLE"""
def mostrar_detalle(biblioteca):
    print("\n--- Detalle de canción ---")
    try:
        id_cancion = int(input("ingrese ID de la canción: ").strip())
        cancion_encontrada = None
        for c in biblioteca._canciones:
            if int(c.id) == id_cancion:
                cancion_encontrada = c
                break
        if cancion_encontrada is None:
            print(f"❌ No se encontro ninguna canción con el ID {id_cancion}.")
        else:
            print(f"\nDetalle de la canción con ID {id_cancion}:")
            print(f"Título: {cancion_encontrada.titulo}")
            print(f"Artista: {cancion_encontrada.artista}")
            print(f"Álbum: {cancion_encontrada.album}")
            print(f"Género: {cancion_encontrada.genero}")
            print(f"Año: {cancion_encontrada.anio}")
            print(f"Duración: {cancion_encontrada.duracion_seg} segundos")
    
    except ValueError:
        print("❌ Error: El ID debe ser un número entero.")


"""3. MENU DE BÚSQUEDA"""
def menu_busqueda(biblioteca):
    while True:
        print("\n--- Búsqueda ---")
        print("1. Búsqueda lineal")
        print("2. Búsqueda binaria (requiere colección ordenada)")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            while True:
                print("\n--- Búsqueda lineal ---")
                print("1. Buscar por ID")
                print("2. Buscar por título")
                print("3. Buscar por artista")
                print("4. Buscar por álbum")
                print("5. Buscar por género")
                print("0. Volver")
                sub_opcion = input("> ").strip()

                if sub_opcion == "0":
                    break
                elif sub_opcion in {"1", "2", "3", "4", "5"}:
                    clave = input("Ingrese la clave a buscar: ").strip()
                    if sub_opcion == "1":
                        resultado = busqueda_lineal(biblioteca.listar(), clave, obtener_clave=lambda c: c.id)
                    elif sub_opcion == "2":
                        resultado = busqueda_lineal(biblioteca.listar(), clave, obtener_clave=lambda c: c.titulo)
                    elif sub_opcion == "3":
                        resultado = busqueda_lineal(biblioteca.listar(), clave, obtener_clave=lambda c: c.artista)
                    elif sub_opcion == "4":
                        resultado = busqueda_lineal(biblioteca.listar(), clave, obtener_clave=lambda c: c.album)
                    elif sub_opcion == "5":
                        resultado = busqueda_lineal(biblioteca.listar(), clave, obtener_clave=lambda c: c.genero)

                    if resultado:
                        print(f"✅ Canción encontrada: {resultado}")
                    else:
                        print("❌ Canción no encontrada.")
                else:
                    print("Opción inválida.")
        elif opcion == "2":
            clave = input("Ingrese la clave a buscar: ").strip()
            # Suponiendo que la colección está ordenada por ID
            resultado = busqueda_binaria(sorted(biblioteca.listar(), key=lambda c: c.id), clave, obtener_clave=lambda c: c.id)
            if resultado:
                print(f"✅ Canción encontrada: {resultado}")
            else:
                print("❌ Canción no encontrada.")
        else:
            print("Opción inválida.")


"""4. MENU DE ORDENAMIENTO"""
def menu_ordenamiento(biblioteca):
    while True:
        print("\n--- Ordenamiento ---")
        print("1. Ordenamiento por selección")
        print("2. Ordenamiento por inserción")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print("\n--- Ordenamiento ---")
            print("1. Ordenar por titulo")
            print("2. Ordenamiento por duración")
            print("3. Ordenamiento por artista")
            print("4. Ordenamiento por albúm")
            print("5. Ordenamiento por género")
            print("0. Volver")
            opcion = input("> ").strip()

            if opcion == "0":
                break
            elif opcion == "1":
                canciones_ordenadas = ordenar_seleccion(biblioteca.listar(), clave=lambda c: c.titulo)
                print("✅ Canciones ordenadas por título (Selección):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "2":
                canciones_ordenadas = ordenar_seleccion(biblioteca.listar(), clave=lambda c: c.duracion_seg)
                print("✅ Canciones ordenadas por duración (Selección):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "3":
                canciones_ordenadas = ordenar_seleccion(biblioteca.listar(), clave=lambda c: c.artista)
                print("✅ Canciones ordenadas por artista (Selección):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "4":
                canciones_ordenadas = ordenar_seleccion(biblioteca.listar(), clave=lambda c: c.album)
                print("✅ Canciones ordenadas por álbum (Selección):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "5":
                canciones_ordenadas = ordenar_seleccion(biblioteca.listar(), clave=lambda c: c.genero)
                print("✅ Canciones ordenadas por género (Selección):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
        elif opcion == "2":
            print("\n--- Ordenamiento ---")
            print("1. Ordenar por titulo")
            print("2. Ordenamiento por duración")
            print("3. Ordenamiento por artista")
            print("4. Ordenamiento por albúm")
            print("5. Ordenamiento por género")
            print("0. Volver")
            opcion = input("> ").strip()

            if opcion == "0":
                break
            elif opcion == "1":
                canciones_ordenadas = ordenar_insercion(biblioteca.listar(), clave=lambda c: c.titulo)
                print("✅ Canciones ordenadas por título (Inserción):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "2":
                canciones_ordenadas = ordenar_insercion(biblioteca.listar(), clave=lambda c: c.duracion_seg)
                print("✅ Canciones ordenadas por duración (Inserción):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "3":
                canciones_ordenadas = ordenar_insercion(biblioteca.listar(), clave=lambda c: c.artista)
                print("✅ Canciones ordenadas por artista (Inserción):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "4":
                canciones_ordenadas = ordenar_insercion(biblioteca.listar(), clave=lambda c: c.album)
                print("✅ Canciones ordenadas por álbum (Inserción):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
            elif opcion == "5":
                canciones_ordenadas = ordenar_insercion(biblioteca.listar(), clave=lambda c: c.genero)
                print("✅ Canciones ordenadas por género (Inserción):")
                for c in canciones_ordenadas:
                    print(f" - {c.titulo} | Artista: {c.artista} | Álbum: {c.album} | Género: {c.genero} | ({c.duracion_seg}s)")
        else:
            print("Opción inválida.")


"""5. FUNCIONES DE BÚSQUEDA Y VERSIONES"""
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
        if v is not None:
            _,tipo = biblioteca.versiones.get(str(id_v))
            print(f" - {v.titulo} ({v.artista}) [version: {tipo}]")


"""6. MENU DE COLECCIONES (1.PLAYLIST - 2.CATALOGO)"""
def menu_colecciones(biblioteca, playlist):
    while True:
        print("\n--- ¿Que colección desea moodificar? ---")
        print("1. Playlist")
        print("2. Catalogo general")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            menu_playlist(biblioteca, playlist)
        elif opcion == "2":
            menu_catalogo(biblioteca)
        else:
            print("Opción inválida.")

"""6.1. MENU DE PLAYLIST (AGREGAR, QUITAR, LISTAR)"""
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

"""6.2. MENU DE CATALOGO (ALTA, MODIFICACION, BAJA)"""
def menu_catalogo(biblioteca,):
    while True:
        print("\n--- ABM Catálogo General (Persistencia E5) ---")
        print("1. Dar de alta una canción nueva")
        print("2. Modificar una canción por ID")
        print("3. Dar de baja una canción por ID")
        print("0. Volver")
        opcion = input("> ").strip()
        
        if opcion == "0":
            break
        elif opcion == "1":
            print("\n--- Alta de canción ---")
            try:
                id_cancion = biblioteca.generar_siguiente_id()
                print(f"ID asignado automáticamente: {id_cancion}")
                titulo = input("Título: ").strip()
                artista = input("Artista: ").strip()
                album = input("Álbum: ").strip()
                genero = input("Género: ").strip()
                anio_str = input("Año: ").strip()
                anio = int(anio_str)
                duracion_str = input("Duración en segundos: ").strip()
                duracion_seg = int(duracion_str)
                nueva_cancion = Cancion(
                    id=id_cancion,
                    titulo=titulo,
                    artista=artista,
                    album=album,
                    genero=genero,
                    anio=anio,
                    duracion_seg=duracion_seg
                )
                
                biblioteca._canciones.insertar_al_final(nueva_cancion)
                alta_binario(RUTA_CANCIONES.with_suffix(".bin"), nueva_cancion)
                guardar_texto(RUTA_CANCIONES, filas_del_catalogo(biblioteca._canciones), ENCABEZADOS)
                print(f"✅ Canción agregada: {nueva_cancion.resumen()}")
            except ValueError:
                print("❌ Error: ID, año y duración deben ser números enteros.")
       
        elif opcion == "2":
            print("\n--- Modificación de canción ---")
            try:
                id_str = input("ID de la canción (número entero): ").strip()
                id_buscado = int(id_str)
                posicion = posicion_del_id(biblioteca._canciones, id_buscado)

                cancion_actual = None
                for c in biblioteca._canciones:
                    if int(c.id) == id_buscado:
                        cancion_actual = c
                        break
                print(f"Modificando: {cancion_actual.resumen()}")
                print("Dejar vacío para mantener el valor actual.")

                nuevo_titulo = input(f"Título [{cancion_actual.titulo}]: ").strip()
                nuevo_artista = input(f"Artista [{cancion_actual.artista}]: ").strip()
                nuevo_album = input(f"Álbum [{cancion_actual.album}]: ").strip()
                nuevo_genero = input(f"Género [{cancion_actual.genero}]: ").strip() 
                nuevo_anio_str = input(f"Año [{cancion_actual.anio}]: ").strip() 
                nuevo_duracion_str = input(f"Duración en segundos [{cancion_actual.duracion_seg}]: ").strip()

                if nuevo_titulo:
                    cancion_actual.titulo = nuevo_titulo
                if nuevo_artista:
                    cancion_actual.artista = nuevo_artista
                if nuevo_album:
                    cancion_actual.album = nuevo_album
                if nuevo_genero:
                    cancion_actual.genero = nuevo_genero
                if nuevo_anio_str:
                    cancion_actual.anio = int(nuevo_anio_str)
                if nuevo_duracion_str:
                    cancion_actual.duracion_seg = int(nuevo_duracion_str)

                actualizar_registro(RUTA_CANCIONES.with_suffix(".bin"), posicion, cancion_actual)
                guardar_texto(RUTA_CANCIONES, filas_del_catalogo(biblioteca._canciones), ENCABEZADOS)
                print(f"✅ Canción modificada: {cancion_actual.resumen()}")

            except ValueError:
                print("❌ Error: ID, año y duración deben ser números enteros.")
            except ItemNoEncontradoError as e:
                print(f"❌ {e}")

        elif opcion == "3":
            print("\n--- Baja de canción ---")
            try:
                id_str = input("ID de la canción a dar de baja (número entero): ").strip()
                id_baja = int(id_str)
                posicion = posicion_del_id(biblioteca._canciones, id_baja)

                cancion_a_borrar = None
                for c in biblioteca._canciones:
                    if int(c.id) == id_baja:
                        cancion_a_borrar = c
                        break

                biblioteca._canciones.eliminar(cancion_a_borrar)
                baja_binario(RUTA_CANCIONES.with_suffix(".bin"), posicion)
                guardar_texto(RUTA_CANCIONES, filas_del_catalogo(biblioteca._canciones), ENCABEZADOS)
                print(f"✅ Canción eliminada: {cancion_a_borrar.resumen()}")
            except ValueError:
                print("❌ Error: ID debe ser un número entero.")
            except ItemNoEncontradoError as e:
                print(f"❌ {e}")


"""7. MENU DE HISTORIAL (PILA)"""
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


"""8. MENU DE COLA DE REPRODUCCIÓN"""
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


"""9. MENU DE GUARDAR / CARGAR ARCHIVOS"""
def menu_guardar_cargar(biblioteca):
    while True:
        print(" 1. Cargar catálogo desde el .txt de la cátedra")
        print(" 2. Guardar catálogo en .txt")
        print(" 3. Guardar catálogo en binario (.bin)")
        print(" 4. Cargar catálogo desde binario (.bin)")
        print(" 0. Volver")
        sub = input(" Subopción > ").strip().lower()
        try:
            if sub == "0":
                break
            elif sub == "1":
                biblioteca._canciones = armar_catalogo_desde_txt(RUTA_CANCIONES)
                print(f"Catálogo cargado: {biblioteca._canciones.tamanio()} ítems.")

            elif sub == "2":
                if hasattr(biblioteca, "_canciones") and biblioteca._canciones is not None:
                    guardar_texto(RUTA_CANCIONES, filas_del_catalogo(biblioteca._canciones), ENCABEZADOS)
                    print("Catálogo guardado en .txt.")
                else:
                    print("Error: Primero debes cargar un catálogo (opción 1).")
            elif sub == "3":
                guardar_binario(RUTA_BIN, biblioteca._canciones)
                print(f"Catálogo guardado en .bin ({biblioteca._canciones.tamanio()} ítems).")
            elif sub == "4":
                catalogo = cargar_binario(RUTA_BIN)
                print(f"Catálogo cargado desde binario: {catalogo.tamanio()} ítems.")
            else:
                print("Subopción inválida.")
        except ArchivoInvalidoError as error:
            print(f"Archivo inválido: {error}")

if __name__ == "__main__":
    main()