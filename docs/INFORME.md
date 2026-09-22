# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

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
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
