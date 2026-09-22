# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que entregan.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6 (pila, cola, archivos, recursión, búsquedas).

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y listar catálogo | Opcion 1 del menú (`data/canciones.txt`) | Lista de canciones no vacía, sin traceback | no corrido | Prueba de listado básico |
| P02 | E1 | Buscar o elegir un ítem inexistente | ID = `-1` | Mensaje claro ("Canción no encontrada"), el menú sigue activo | no corrido | Manejo de IDs inválidos |
| P03 | E2 | Operación recursiva sobre un ítem con cadena | ID = `12` | Imprime las versiones derivadas (`[13]`) | no corrido | Prueba del caso recursivo con derivadas |
| P04 | E2 | Operación recursiva sobre un ítem sin derivados | ID = `13` | Muestra lista vacía `[]` o mensaje sin versiones (caso base) | no corrido | Prueba del caso base |
| P05_E2 | E2 | Ver detalle completo de una canción existente | ID = `1` | Muestra título, artista y atributos completos de la canción | no corrido | Consulta de detalle por ID |
| P06_E2 | E2 | Elegir una opción inválida del menú principal | Opción = `"99z"` | Mensaje de opción inválida, el menú vuelve a mostrarse | no corrido | Validación de entrada en menú |
| P07_E2 | E2 | Enviar una entrada vacía en el menú | Presionar Enter directamente (`""`) | No genera excepción, vuelve a solicitar una opción | no corrido | Robustez de lectura en consola |
| P08_E2 | E2 | Buscar una canción con texto en blanco/espacios | Término = `"   "` | Mensaje de aviso de búsqueda inválida y menú activo | no corrido | Manejo de espacios en blanco |
| P05 | E3 | Agregar a la colección principal hasta el tope | equipo de 6 / equivalente | el séptimo falla con excepción propia |  |  |
| P06 | E3 | Desapilar historial vacío | pila vacía | excepción propia, menú sigue |  |  |
| P07 | E3 | Desencolar cola vacía | cola vacía | excepción propia, menú sigue |  |  |
| P08 | E3 | Listar colección con el iterador | 2+ ítems | el orden coincide con las inserciones |  |  |
| P09 | E4 | Búsqueda lineal de un nombre que existe |  | lo encuentra |  |  |
| P10 | E4 | Búsqueda lineal de un nombre que no existe |  | no encontrado, sin traceback |  |  |
| P11 | E4 | Búsqueda binaria con catálogo desordenado |  | avisa o reordena; no da un falso hit |  |  |
| P12 | E4 | Ordenar por un criterio y después por otro |  | el orden cambia |  |  |
| P13 | E5 | Guardar CSV, salir, volver a entrar |  | los datos siguen |  |  |
| P14 | E5 | Guardar binario y modificar un registro por id |  | al recargar, ese campo cambió |  |  |
| P15 | E5 | Abrir un binario truncado o con magia mala | archivo basura | excepción de archivo inválido |  |  |
