# AyED C2 2026 — Biblioteca musical — Grupo 45

Integrantes: Martina Zamorano (zamoranomartina07), Andrea Lescano Muñoz (andrealescano200226-source), Emiliano German Gomez (emigerman)

## Cómo ejecutarlo
Requiere Python 3.10+ (solo biblioteca estándar). Desde la raíz del repo:

    python -m src.main

## Tema
Biblioteca musical: catálogo de canciones con sus versiones (covers, remixes, en vivo), donde una canción puede ser versión de otra.

## Qué hace
Gestor de catálogo por consola con las 10 operaciones: listar, ver detalle,
buscar (lineal y binaria), ordenar (selección e inserción), recursión de
versiones (todas las versiones derivadas de una canción, en cualquier nivel),
ABM de una playlist con tope de 6 canciones, historial de acciones (pila),
cola de reproducción, y persistencia en CSV y binario con struct.

## Limitaciones conocidas
- La búsqueda binaria solo funciona si antes se ordenó el catálogo.
- Las búsquedas son por coincidencia exacta: no ignoran mayúsculas, tildes ni texto parcial.
- Todo funciona por consola, sin interfaz gráfica.
