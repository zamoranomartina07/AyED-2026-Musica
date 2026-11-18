# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

###Grupo 45 Comision 1

| Nombre | Mail | GitHub |
| --- | --- | --- |
| Martina Zamorano | zamoranomartina07@gmail.com | zamoranomartina07 |
|  Andrea Lescano Muñoz  | andrealescano200226@gmail.com |andrealescano200226-source |
| Emiliano German Gomez | emilianog.gomez@outlook.com | emigerman |

- Tema: Musica
- Por qué lo eligieron : Elegimos el tema **Biblioteca Musical** porque nos permite modelar una estructura clara y realista de datos interactivos sobre un tema de interes de los integrantes del grupo


## 2. Modelo

## Ítem del Catálogo
Un ítem del catálogo es una **Canción** (`Cancion`), que representa una pista de audio en la biblioteca. Sus atributos principales son:
* `id` (identificador único)
* `titulo`
* `artista`
* `album`
* `genero`
* `duracion_seg` (duración en segundos)

---

## Mutabilidad e Inmutabilidad (E1)

### Datos Inmutables
* **ID (`id`):** Es el identificador único de la canción. No cambia a lo largo del tiempo para preservar la integridad de las referencias.
* **Duración (`duracion_seg`):** Es un valor fijo inherente al archivo o grabación de la pista.

### Datos Mutables
* **Metadatos de la Canción (`titulo`, `artista`, `album`, `genero`):** Pueden modificarse si el usuario edita o corrige la información de una pista.
* **Colecciones y Estructuras:** El catálogo global, la playlist principal, el historial y la cola de reproducción son estructuras dinámicas que cambian continuamente al agregar, eliminar o reordenar canciones.

## 3. Recursión (E2)

- **Función:** `versiones_de(versionable, id_cancion)`
- **Caso base:** Si la canción no tiene versiones derivadas en `versiones.txt`, devuelve una lista vacía `[]`.
- **Caso recursivo:** Obtiene las versiones directas, hace la llamada recursiva para cada una y concatena los resultados.

### Traza de un ejemplo real del dataset
**Ejemplo probado:** Buscar todas las versiones derivadas de la Canción ID `12`.  
**Datos reales de `data/versiones.txt`:**  
* `13,12,live` (la canción 13 es un Live de la 12)

**Llamadas recursivas (Apilado):**
1. `versiones_de(12)` $\rightarrow$ versión directa encontrada: `13`. Llama a `[13] + versiones_de(13)`.
2. `versiones_de(13)` $\rightarrow$ no tiene versiones derivadas registradas. **Alcanza el Caso Base** y devuelve `[]`.

**Resolución de retorno (Desapilado):**
* Retorno de `versiones_de(13)`: `[]`
* Retorno de `versiones_de(12)`: `[13] + []` = `[13]`

**Resultado final:** `[13]`

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
| Listar catálogo | O(n) | O(1) | Recorre cada elemento una sola vez, sin copiar nada. |
| Búsqueda lineal | O(n) | O(1) | En el peor caso (no existe) compara contra los n elementos. |
| Búsqueda binaria | O(log n) | O(1) | Descarta la mitad de la colección en cada paso: hacen falta log₂ n pasos. |
| Ordenar por selección | O(n²) | O(n) | Dos bucles anidados que siempre se ejecutan completos; el O(n) es la copia que devuelve. |
| Ordenar por inserción | O(n²) | O(n) | Peor caso (lista inversa): cada elemento se compara con todos los anteriores. Mejor caso (ya ordenada): O(n). |
| Pila (apilar/desapilar) | O(1) | O(1) | Solo se toca el tope, sin recorrer nada. |
| Cola: encolar | O(n) | O(1) | Usa insertar_al_final de la lista enlazada, que recorre todos los nodos hasta el último porque no hay puntero al final. |
| Cola: desencolar | O(1) | O(1) | El frente es la cabeza de la lista: se lee y se elimina sin recorrer. |
| Lista enlazada: insertar al inicio | O(1) | O(1) | Solo se crea un nodo y se cambia la cabeza. |
| Lista enlazada: insertar al final | O(n) | O(1) | Recorre hasta el último nodo, no hay puntero al final. |
| Lista enlazada: insertar ordenado | O(n) | O(1) | Recorre hasta encontrar la posición según la clave. |
| Lista enlazada: buscar / eliminar | O(n) | O(1) | Recorre nodo por nodo; en el peor caso el dato está al final o no existe. |
| Lista enlazada: recorrer | O(n) | O(1) | Visita cada nodo una vez. |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| Busqueda Lineal (nombre) | 3 | 0.000005 |
| Busqueda Lineal (n x 10) | 30 | 0.000006 |
| Busqueda Lineal (n x 1000) | 3000 | 0.000156 |
| Busqueda binaria (nombre) | 3 | 0.000004 |
| Busqueda binaria (n x 10) | 30 | 0.000004 |
| Busqueda binaria (n x 1000) | 3000 | 0.000008 |

## 6. Persistencia (E5)

- Layout del registro binario: `struct.Struct("<I 30s 25s 30s 12s 2H")` = 105 bytes.
  `id` (I, 4 B), `titulo` (30 B), `artista` (25 B), `album` (30 B), `genero` (12 B), `anio` y `duracion_seg` (H, 2 B c/u). Cadenas UTF-8 recortadas/rellenadas con `\x00` al ancho fijo.
- Header: `struct.Struct("<4s 1s I")` = 9 bytes: magia `AYED`, tema `M`, cantidad de registros.
- Actualización por posición: `seek(HEADER.size + posicion * FORMATO.size)` y se pisa ese único registro (acceso directo, O(1)). El alta hace append al final y arregla la cantidad del header. La baja reescribe el archivo sin ese registro.

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
| Martina Zamorano | Esqueleto, catalogo a mano y carga de versiones a biblioteca.py,  |  |
| Andrea Lescano | cancion.py, catalogo.py, biblioteca.py, cola_reproduccion.py, historial.py, playlist.py, ordenamiento.py, tabla de complejidad y readme de producto | | 
| Emiliano Gomez | ordenamiento.py , busqueda.py, binario.py, texto.py  | ordenamiento, busqueda lineal y binaria, carga persistencia de datos en archivo .csv y .bin |