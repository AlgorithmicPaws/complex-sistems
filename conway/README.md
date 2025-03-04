# Conway's Game of Life

Conway's Game of Life es un autómata celular ideado por el matemático John Conway. El juego consiste en una cuadrícula de celdas que pueden vivir, morir o multiplicarse según un conjunto de reglas. El conjunto de reglas estándar, conocido como B3/S23, establece que:

- Una celda viva con 2 o 3 vecinas vivas sobrevive (S23).
- Una celda muerta con exactamente 3 vecinas vivas se convierte en una celda viva (B3).
- Todas las demás celdas vivas mueren en la siguiente generación, y todas las demás celdas muertas permanecen muertas.

En esta versión modificada, para crear deslizadores (gliders) con estructuras más pequeñas, el conjunto de reglas cambia a B2/S23:

- Una celda viva con 2 o 3 vecinas vivas sobrevive (S23).
- Una celda muerta con exactamente 2 vecinas vivas se convierte en una celda viva (B2).
- Todas las demás celdas vivas mueren en la siguiente generación, y todas las demás celdas muertas permanecen muertas.

---

## Cómo Usar:
- **Exportar Patrón (tecla E):** Presiona la tecla E para escribir las coordenadas de las celdas vivas actuales en "pattern.txt".
- **Importar Patrón (tecla I):** Presiona la tecla I para leer "pattern.txt" y superponer su patrón en la cuadrícula.

### Controles Básicos:
- **Clic Izquierdo del Ratón:** Añadir celdas vivas.
- **Clic Derecho del Ratón:** Añadir celdas muertas.
- **Rueda del Ratón:** Acercar/alejar.
- **ESPACIO:** Pausar o reanudar la simulación.
- **C:** Limpiar la cuadrícula.
- **R:** Reiniciar la cuadrícula.
