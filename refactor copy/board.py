import os
from Entities import Pacman, Fantasma, Dot, SuperDot


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
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
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


    def getAdj(self, x, y):
        adjacentes = []
        filas = len(self.tablero)
        columnas = len(self.tablero[0])

        # Verificar las celdas adyacentes (izquierda, derecha, arriba, abajo)
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
            dots = [entidad for entidad in self.entities if isinstance(entidad, Dot)]
            super_dots = [entidad for entidad in self.entities if isinstance(entidad, SuperDot)]

            if pacman and any(fantasma.coord == pacman.coord for fantasma in fantasmas):
                print("¡Pac-Man ha sido atrapado por un fantasma! Fin del juego.")
                return True  # Fin del juego en caso de colisión con fantasma

            # Verificar colisión con dots
            for dot in dots:
                if dot.coord == pacman.coord:
                    self.entities.remove(dot)  # Eliminar el dot cuando Pac-Man lo come

            # Verificar colisión con super dots
            for super_dot in super_dots:
                if super_dot.coord == pacman.coord:
                    self.entities.remove(super_dot)  # Eliminar el super dot
                    pacman.activate_super_power([fantasma for fantasma in self.entities if isinstance(fantasma, Fantasma)])  # Pasa la lista de fantasmas


            return False

    def update(self):
        if self.verificar_colision():
            exit()  # Termina el juego si hay colisión
        for entidad in self.entities:
            if isinstance(entidad, Pacman):
                entidad.update(self, [fantasma for fantasma in self.entities if isinstance(fantasma, Fantasma)])
            else:
                entidad.update(self)

