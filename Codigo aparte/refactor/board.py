import os
from Entities import Pacman, Fantasma


class board:
    def __init__(self):
        self.tablero = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    
        self.grafo_adyacencias = self.generar_lista_adyacencias(self.tablero)
        
        for key, value in self.grafo_adyacencias.items():
            print(f"{key}: {value}")
        
        self.region_bounds = {
            "superior_izquierda": ((1, 1), (9, 6)),          # Rango válido
            "superior_derecha": ((9, 1), (17, 8)),           # Corregido: min_x=9, max_x=17, min_y=1, max_y=8
            "inferior_izquierda": ((11, 1), (17, 9)),        # Rango válido
            "inferior_derecha": ((11, 6), (17, 17))          # Rango válido
        }

        self.entities = []


    def limpiar_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Función que busca la tupla en la lista de instancias
    def buscar_coord(self, coord):
        for entidad in self.entities:
            if entidad.coord == coord:
                return entidad  # Devuelve la tupla si la encuentra
        return None  # Devuelve None si no existe

    def draw(self):
        PARED = "\033[34m██\033[0m"  # Pared azul
        CAMINO = "\033[40m  \033[0m"  # Fondo negro

        for y, row in enumerate(self.tablero):
            for x, cell in enumerate(row):
                foo = self.buscar_coord((x, y))  # Usa (x, y) como coordenadas

                if foo is not None:
                    foo.draw()

                elif cell == 0:
                    print(PARED, end="")
                else:
                    print(CAMINO, end="")

            print()


    def get_line_of_sight(self, start, end):
        if start[0] == end[0]:  # Mismo x, movimiento vertical
            return [(start[0], y) for y in range(min(start[1], end[1]) + 1, max(start[1], end[1]))]
        elif start[1] == end[1]:  # Mismo y, movimiento horizontal
            return [(x, start[1]) for x in range(min(start[0], end[0]) + 1, max(start[0], end[0]))]
        return []

    def get_region_center(self, region):
        centers = {
            "superior_izquierda": (4, 4),
            "superior_derecha": (14, 4),
            "inferior_izquierda": (4, 14),
            "inferior_derecha": (14, 14)
        }
        return centers[region]

    def getAdj(self, x, y):
        adjacentes = []
        filas = len(self.tablero)
        columnas = len(self.tablero[0])

        # Sólo consideramos los movimientos cardinales (derecha, izquierda, arriba, abajo)
        if x - 1 >= 0 and self.tablero[y][x - 1] == 1:  # Izquierda
            adjacentes.append((x - 1, y))
        if x + 1 < columnas and self.tablero[y][x + 1] == 1:  # Derecha
            adjacentes.append((x + 1, y))
        if y - 1 >= 0 and self.tablero[y - 1][x] == 1:  # Arriba
            adjacentes.append((x, y - 1))
        if y + 1 < filas and self.tablero[y + 1][x] == 1:  # Abajo
            adjacentes.append((x, y + 1))

        return adjacentes


    def generar_lista_adyacencias(self, tilemap):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacency_list = {}

        rows = len(tilemap)
        cols = len(tilemap[0])

        for y in range(rows):
            for x in range(cols):
                if tilemap[y][x] == 1:
                    adjacency_list[(x, y)] = []

                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy

                        if 0 <= nx < cols and 0 <= ny < rows and tilemap[ny][nx] == 1:
                            adjacency_list[(x, y)].append((nx, ny))

        return adjacency_list

    
    
    def getGrafo(self):
        return self.grafo_adyacencias
    
    def getTablero(self):
        return self.tablero
    

    def verificar_colision(self):
        pacman = next((entidad for entidad in self.entities if isinstance(entidad, Pacman)), None)
        fantasmas = [entidad for entidad in self.entities if isinstance(entidad, Fantasma)]

        if pacman:
            for fantasma in fantasmas:
                # Verifica si Pac-Man está en una posición adyacente específica
                if self.esta_en_posicion_adyacente(fantasma.coord, pacman.coord):
                    print("¡Pac-Man ha sido atrapado por un fantasma! Fin del juego.")
                    return True  # Fin del juego en caso de colisión
        return False

    def esta_en_posicion_adyacente(self, fantasma_pos, pacman_pos):
        """Verifica si Pac-Man está directamente al frente, atrás, a la izquierda o derecha del fantasma."""
        x_f, y_f = fantasma_pos
        x_p, y_p = pacman_pos

        # Comprueba posiciones adyacentes específicas (derecha, izquierda, arriba, abajo)
        adyacentes_especificos = [
            (x_f + 1, y_f),  # Derecha
            (x_f - 1, y_f),  # Izquierda
            (x_f, y_f + 1),  # Abajo
            (x_f, y_f - 1)   # Arriba
        ]

        return pacman_pos in adyacentes_especificos

    def get_fantasmas_adyacentes(self, region):
        """Devuelve los fantasmas en las regiones adyacentes a la región dada."""
        regiones_adyacentes = {
            "Superior izquierda": ["Superior derecha", "Inferior izquierda"],
            "Superior derecha": ["Superior izquierda", "Inferior derecha"],
            "Inferior izquierda": ["Superior izquierda", "Inferior derecha"],
            "Inferior derecha": ["Superior derecha", "Inferior izquierda"]
        }

        adyacentes = []
        for fantasma in self.entities:
            if isinstance(fantasma, Fantasma) and fantasma.region in regiones_adyacentes[region]:
                adyacentes.append(fantasma)
        return adyacentes


    def update(self):
        pacman = next((entidad for entidad in self.entities if isinstance(entidad, Pacman)), None)
        pacman_coord = pacman.coord if pacman else None

        if self.verificar_colision():
            exit()  # Termina el juego si hay colisión

        # Disminuye las iteraciones de conocimiento de Pac-Man para todos los fantasmas después de actualizar sus movimientos
        for entidad in self.entities:
            if isinstance(entidad, Fantasma):
                # Aquí se pasa `self` en lugar de `self.tablero`
                entidad.decrement_knowledge(self)

        # Primero, los fantasmas actualizan su estado de alerta y sus movimientos
        for entidad in self.entities:
            if isinstance(entidad, Fantasma):
                # Almacenamos la posición inicial del fantasma antes de moverse
                print(f"{entidad.name} posición inicial: {entidad.coord}")

                other_ghosts = [ghost for ghost in self.entities if isinstance(ghost, Fantasma) and ghost != entidad]

                # Verificación de visibilidad directa de Pac-Man y comunicación con otros fantasmas
                if entidad.is_pacman_in_sight(pacman_coord, self):
                    entidad.see_pacman(pacman_coord, self)
                    entidad.alert_adjacent_ghosts(other_ghosts)

                # El fantasma realiza su movimiento (siempre se mueve en cada actualización)
                entidad.move(pacman_coord, self, other_ghosts)

                # Imprime la nueva posición del fantasma después de moverse
                print(f"{entidad.name} nueva posición: {entidad.coord}")

        # Luego, Pac-Man se mueve
        if pacman:
            pacman.update(self)

