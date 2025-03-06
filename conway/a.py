import pygame
import numpy as np

class Tablero:
    # Parámetros de la pantalla y del tablero
    ancho, alto = 700, 400         # Dimensiones totales de la ventana
    celdas = 25                    # Tamaño (en píxeles) de cada celda
    # El área del tablero se dibuja en la parte izquierda; se reserva 100 px a la derecha para los botones
    cantidad_ancho = 0             # Cantidad de celdas en dirección horizontal
    cantidad_alto = 0              # Cantidad de celdas en dirección vertical
    velocidad = 10                 # Velocidad (fps)

    # Matrices del autómata
    tablero_inicial = None
    tablero_general = None

    # Estados del juego
    pausa = None
    paso_a_paso = None

    clock = None       # Controlador de tiempo de pygame
    pantalla = None    # Superficie de dibujo

    # Botones de la interfaz
    boton_inicio = None
    boton_borrar = None
    boton_pasos = None

    # Variables para el reloj digital
    hours = 0
    minutes = 0

    # Patrón para cada dígito (matriz 5x3) – se usarán para inyectar el reloj
    digit_patterns = {
        '0': np.array([[1,1,1],
                       [1,0,1],
                       [1,0,1],
                       [1,0,1],
                       [1,1,1]]),
        '1': np.array([[0,1,0],
                       [1,1,0],
                       [0,1,0],
                       [0,1,0],
                       [1,1,1]]),
        '2': np.array([[1,1,1],
                       [0,0,1],
                       [1,1,1],
                       [1,0,0],
                       [1,1,1]]),
        '3': np.array([[1,1,1],
                       [0,0,1],
                       [1,1,1],
                       [0,0,1],
                       [1,1,1]]),
        '4': np.array([[1,0,1],
                       [1,0,1],
                       [1,1,1],
                       [0,0,1],
                       [0,0,1]]),
        '5': np.array([[1,1,1],
                       [1,0,0],
                       [1,1,1],
                       [0,0,1],
                       [1,1,1]]),
        '6': np.array([[1,1,1],
                       [1,0,0],
                       [1,1,1],
                       [1,0,1],
                       [1,1,1]]),
        '7': np.array([[1,1,1],
                       [0,0,1],
                       [0,1,0],
                       [0,1,0],
                       [0,1,0]]),
        '8': np.array([[1,1,1],
                       [1,0,1],
                       [1,1,1],
                       [1,0,1],
                       [1,1,1]]),
        '9': np.array([[1,1,1],
                       [1,0,1],
                       [1,1,1],
                       [0,0,1],
                       [1,1,1]])
    }

    # Posiciones (en índice de celdas) donde se mostrarán los dígitos.
    # Importante: en este tablero, la matriz "tablero_general" se indexa como [i, j]
    # donde "i" representa la posición horizontal (x) y "j" la vertical (y).
    # Se definieron las posiciones de forma que cada dígito (5 filas x 3 columnas) quepa en el área de juego.
    digit_positions = {
        "hour_tens": (3, 5),     # (x, y)
        "hour_ones": (7, 5),
        "minute_tens": (13, 5),
        "minute_ones": (17, 5)
    }
    # Posición para el ":" (se usarán dos celdas verticalmente)
    colon_position = (11, 5)

    def _init_(self, ancho=700, alto=400, celdas=25, velocidad=10):
        self.ancho = ancho
        self.alto = alto
        self.celdas = celdas
        self.velocidad = velocidad
        # Se reserva 100 px a la derecha para botones, por lo que el área del tablero es (ancho-100)
        self.cantidad_ancho = (self.ancho - 100) // self.celdas
        self.cantidad_alto = self.alto // self.celdas

    def start(self):
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life - Reloj Digital")
        self.clock = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        # Inicializamos el tablero con todas las celdas muertas
        self.tablero_inicial = np.zeros((self.cantidad_ancho, self.cantidad_alto))
        self.tablero_general = np.copy(self.tablero_inicial)
        self.pausa = True
        self.paso_a_paso = False
        # Definir botones (ubicados en la parte derecha)
        self.boton_inicio = pygame.Rect(self.ancho - 90, 10, 80, 30)
        self.boton_borrar = pygame.Rect(self.ancho - 90, 50, 80, 30)
        self.boton_pasos = pygame.Rect(self.ancho - 90, 90, 80, 30)
        # Reiniciar el reloj
        self.hours = 0
        self.minutes = 0

    def imprint_digit(self, digit, top_left):
        """
        Inyecta el patrón del dígito (5x3) en 'tablero_general' a partir de la posición top_left.
        top_left es una tupla (x, y) en índice de celdas.
        """
        pattern = self.digit_patterns[digit]
        rows, cols = pattern.shape  # rows: vertical, cols: horizontal
        for r in range(rows):
            for c in range(cols):
                # En la matriz, el primer índice es la posición horizontal (x) y el segundo la vertical (y)
                self.tablero_general[top_left[0] + c, top_left[1] + r] = pattern[r, c]

    def imprint_colon(self, top_left):
        """
        Inyecta el ":" en 'tablero_general'. Se activan dos celdas: una en top_left y otra dos celdas más abajo.
        """
        self.tablero_general[top_left[0], top_left[1]] = 1
        self.tablero_general[top_left[0], top_left[1] + 2] = 1

    def overlay_clock(self):
        """
        Limpia la zona donde se muestran los dígitos y luego inyecta los patrones correspondientes
        según la hora actual (self.hours y self.minutes).
        """
        # Limpiar áreas de cada dígito (cada dígito ocupa 3 columnas x 5 filas)
        for pos in self.digit_positions.values():
            for c in range(3):
                for r in range(5):
                    self.tablero_general[pos[0] + c, pos[1] + r] = 0
        # Limpiar área del colon (se asume 1 columna x 3 filas)
        x, y = self.colon_position
        for r in range(3):
            self.tablero_general[x, y + r] = 0

        # Convertir la hora actual a dos dígitos
        hour_str = f"{self.hours:02d}"
        minute_str = f"{self.minutes:02d}"
        self.imprint_digit(hour_str[0], self.digit_positions["hour_tens"])
        self.imprint_digit(hour_str[1], self.digit_positions["hour_ones"])
        self.imprint_digit(minute_str[0], self.digit_positions["minute_tens"])
        self.imprint_digit(minute_str[1], self.digit_positions["minute_ones"])
        self.imprint_colon(self.colon_position)

    def update_clock(self):
        """
        Actualiza el reloj: se incrementa el minuto; si llega a 60, se reinicia y se incrementa la hora.
        Si la hora llega a 24, se reinicia.
        """
        self.minutes += 1
        if self.minutes >= 60:
            self.minutes = 0
            self.hours += 1
            if self.hours >= 24:
                self.hours = 0

    def reglas(self):
        """
        Aplica las reglas del Juego de la Vida y actualiza el reloj.
        Se calcula la cantidad de vecinos para cada celda y se actualiza el estado.
        """
        tablero_nuevo = np.zeros_like(self.tablero_general)
        for i in range(1, self.cantidad_ancho - 1):
            for j in range(1, self.cantidad_alto - 1):
                # Calcular vecinos (suma de la vecindad menos la celda actual)
                cantidad_vecinos = np.sum(self.tablero_general[i-1:i+2, j-1:j+2]) - self.tablero_general[i, j]
                if self.tablero_general[i, j] == 1 and (cantidad_vecinos < 2 or cantidad_vecinos > 3):
                    tablero_nuevo[i, j] = 0
                elif self.tablero_general[i, j] == 0 and cantidad_vecinos == 3:
                    tablero_nuevo[i, j] = 1
                else:
                    tablero_nuevo[i, j] = self.tablero_general[i, j]
        self.tablero_general = tablero_nuevo
        # Actualizar el reloj (se incrementa un "tic" en cada actualización)
        self.update_clock()
        # Inyectar (o actualizar) los dígitos del reloj en la cuadrícula
        self.overlay_clock()

    def dibujar_cuadricula(self):
        
        # Actualizamos la zona del reloj antes de dibujar
        self.overlay_clock()
        self.pantalla.fill((44, 44, 44))
        # Dibujar cada celda del tablero
        for i in range(self.cantidad_ancho):
            for j in range(self.cantidad_alto):
                if self.tablero_general[i, j] == 1:
                    pygame.draw.rect(self.pantalla, (27, 140, 255),
                                     (i * self.celdas, j * self.celdas, self.celdas, self.celdas))
                else:
                    pygame.draw.rect(self.pantalla, (53, 53, 53),
                                     (i * self.celdas, j * self.celdas, self.celdas, self.celdas))
        # Dibujar líneas de la cuadrícula
        for i in range(0, self.cantidad_ancho * self.celdas, self.celdas):
            pygame.draw.line(self.pantalla, (210, 210, 210), (i, 0), (i, self.alto))
        for j in range(0, self.cantidad_alto * self.celdas, self.celdas):
            pygame.draw.line(self.pantalla, (210, 210, 210), (0, j), (self.cantidad_ancho * self.celdas, j))
        # Dibujar los botones (en la parte derecha)
        pygame.draw.rect(self.pantalla, (101, 248, 161), self.boton_inicio)
        pygame.draw.rect(self.pantalla, (255, 93, 72), self.boton_borrar)
        pygame.draw.rect(self.pantalla, (72, 187, 255), self.boton_pasos)

        # Dibujar textos en los botones
        font1 = pygame.font.Font(None, 35)
        font2 = pygame.font.Font(None, 35)
        font3 = pygame.font.Font(None, 35)
        texto_inicio = font1.render("Inicio", True, (0, 0, 0))
        texto_borrar = font2.render("Borrar", True, (0, 0, 0))
        texto_pasos = font3.render("Pasos", True, (0, 0, 0))
        self.pantalla.blit(texto_inicio, (self.ancho - 83, 15))
        self.pantalla.blit(texto_borrar, (self.ancho - 87, 55))
        self.pantalla.blit(texto_pasos, (self.ancho - 86, 95))

        pygame.display.flip()


class Juego:
    def _init_(self):
        self.tablero = Tablero()

    def start(self):
        self.tablero.start()
        self.tablero.dibujar_cuadricula()

    def reglas(self):
        self.tablero.reglas()

    def play(self):
        self.start()
        ejecucion = True
        while ejecucion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecucion = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Verificar si se hizo clic en alguno de los botones
                    if self.tablero.boton_inicio.collidepoint(event.pos):
                        self.tablero.pausa = not self.tablero.pausa
                        self.tablero.paso_a_paso = False
                    elif self.tablero.boton_borrar.collidepoint(event.pos):
                        self.tablero.tablero_general = np.copy(self.tablero.tablero_inicial)
                        self.tablero.paso_a_paso = False
                        self.tablero.pausa = True
                        self.tablero.hours = 0
                        self.tablero.minutes = 0
                    elif self.tablero.boton_pasos.collidepoint(event.pos):
                        self.tablero.paso_a_paso = True
                        self.tablero.pausa = False
                    else:
                        # Si se hace clic en el área del tablero, se alterna el estado de la celda clickeada
                        x, y = event.pos
                        # Asegurarse de que el clic se encuentre en el área del tablero (sin incluir el panel de botones)
                        if x < self.tablero.cantidad_ancho * self.tablero.celdas and y < self.tablero.cantidad_alto * self.tablero.celdas:
                            i, j = x // self.tablero.celdas, y // self.tablero.celdas
                            self.tablero.tablero_general[i, j] = 1 - self.tablero.tablero_general[i, j]

            # Si no está en pausa se actualiza la simulación
            if not self.tablero.pausa:
                self.reglas()
                if self.tablero.paso_a_paso:
                    self.tablero.pausa = True

            self.tablero.dibujar_cuadricula()
            self.tablero.clock.tick(self.tablero.velocidad)

        pygame.quit()


if __name__ == "_main_":
    juego = Juego()
    juego.play()