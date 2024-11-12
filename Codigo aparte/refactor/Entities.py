from collections import deque
import heapq
import random

region_limits = {
    "superior_izquierda": ((0, 0), (8, 8)),
    "superior_derecha": ((9, 0), (19, 8)),
    "inferior_izquierda": ((0, 9), (8, 19)),
    "inferior_derecha": ((9, 9), (19, 19))
}

class Entities:
    def __init__(self, color, coord, player=False):
        self.color = color
        self.coord = coord
        self.player = player

    def update(self, board):
        pass

    def draw(self):
        print(self.color, end="")

    def heuristica(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


import random

class Fantasma(Entities):
    def __init__(self, nombre, color, coord, region):
        super().__init__(color, coord)  # Llamada al constructor de Entities
        self.name = nombre
        self.region = region
        self.alerted = False
        self.home_region = coord
        self.target_coord = None
        self.pacman_knowledge = {"position": None, "iterations": 0}

    def move(self, pacman_pos, board, other_ghosts=None):
        nueva_pos = self.coord
        objetivo = pacman_pos

        # Si el fantasma tiene conocimiento de Pac-Man, usa esa posición como objetivo
        if self.pacman_knowledge["iterations"] > 0:
            objetivo = self.pacman_knowledge["position"]
        elif not self.alerted:
            # Si el fantasma no está en alerta, usa un objetivo aleatorio en su región
            if self.target_coord is None or self.coord == self.target_coord:
                # Define un nuevo objetivo aleatorio dentro de los límites de la región
                self.target_coord = self.get_random_valid_position(board)
            objetivo = self.target_coord

        # Determina el tipo de movimiento del fantasma basado en si está en alerta
        if self.alerted:
            if self.name == "BLINKY":
                nueva_pos = self.greedy_bfs(objetivo, board)
            elif self.name == "PINKY":
                nueva_pos = self.bidirectional_search(objetivo, board)
            elif self.name == "INKY":
                nueva_pos = self.a_star(objetivo, board)
            elif self.name == "CLYDE":
                nueva_pos = self.bfs(objetivo, board)
        else:
            # Mueve hacia el objetivo aleatorio dentro de su región
            nueva_pos = self.move_randomly_in_region(board)

        # Verifica que la nueva posición no sea una pared antes de actualizar la posición
        if self.is_wall(board, nueva_pos):
            # Si el objetivo es una pared, buscamos un nuevo objetivo válido
            nueva_pos = self.get_random_valid_position(board)

        # Evita colisiones con otros fantasmas
        if other_ghosts and any(ghost.coord == nueva_pos for ghost in other_ghosts):
            nueva_pos = self.coord  # Se mantiene en su posición anterior si hay colisión

        # Actualiza la posición
        self.coord = nueva_pos

    def is_wall(self, board, coord):
        """Verifica si la coordenada dada es una pared."""
        x, y = coord
        if 0 <= y < len(board.tablero) and 0 <= x < len(board.tablero[0]):
            return board.tablero[y][x] == 0  # 0 representa una pared
        return True  # Si está fuera de los límites, lo tratamos como si fuera una pared

    def get_random_valid_position(self, board):
        """Genera una posición aleatoria que no sea una pared."""
        x, y = self.coord
        valid_positions = []

        # Revisamos las posiciones adyacentes
        for nx, ny in board.getAdj(x, y):
            if not self.is_wall(board, (nx, ny)):  # Si no es una pared, es válida
                valid_positions.append((nx, ny))

        # Si hay posiciones válidas, elegimos una aleatoriamente
        if valid_positions:
            return random.choice(valid_positions)
        else:
            return self.coord  # Si no hay posiciones válidas, mantenemos la posición actual

    def decrement_knowledge(self, board):
        """Disminuye las iteraciones restantes del conocimiento de Pac-Man."""
        if self.pacman_knowledge["iterations"] > 0:
            self.pacman_knowledge["iterations"] -= 1
            print(f"{self.name}: Iteraciones restantes con conocimiento de Pac-Man: {self.pacman_knowledge['iterations']}")
        
        # Si se acaban las iteraciones, desactiva la alerta y establece el objetivo en su región de origen
        if self.pacman_knowledge["iterations"] == 0:
            self.alerted = False
            self.target_coord = board.get_region_center(self.region)  # Establece el objetivo a la región de origen
            print(f"{self.name} ha perdido el rastro de Pac-Man y vuelve a su región de origen.")


    def see_pacman(self, pacman_pos, board):
        if self.pacman_knowledge["position"] != pacman_pos:
            self.pacman_knowledge["position"] = pacman_pos
            self.pacman_knowledge["iterations"] = 8
            self.alerted = True
            print(f"{self.name} ha visto a Pac-Man en {pacman_pos} y mantendrá esta posición por 8 iteraciones.")

    def move_randomly_in_region(self, board):
        """Mueve el fantasma aleatoriamente dentro de su región de origen."""
        region_min, region_max = region_limits[self.region]
        direcciones = board.getAdj(self.coord[0], self.coord[1])

        # Filtra las direcciones que están dentro de la región
        direcciones_validas = [
            d for d in direcciones
            if region_min[0] <= d[0] <= region_max[0] and region_min[1] <= d[1] <= region_max[1]
        ]

        # Escoge una dirección aleatoria dentro de la región, o se queda en su lugar si no hay direcciones válidas
        return random.choice(direcciones_validas) if direcciones_validas else self.coord


    def is_pacman_in_sight(self, pacman_pos, board):
        px, py = pacman_pos
        gx, gy = self.coord
        if px == gx or py == gy:  # En la misma fila o columna
            line_of_sight = board.get_line_of_sight(self.coord, pacman_pos)
            if all(board.tablero[cell[1]][cell[0]] != 0 for cell in line_of_sight):  # Sin obstáculos
                return True
        return False

    
    def alert_adjacent_ghosts(self, other_ghosts):
        """Alerta a los fantasmas en las regiones adyacentes."""
        for ghost in other_ghosts:
            if self.is_adjacent_region(ghost.region):
                ghost.alert_pacman_position(self.pacman_knowledge["position"])

    def is_adjacent_region(self, other_region):
        adyacentes = {
            "superior_izquierda": ["superior_derecha", "inferior_izquierda"],
            "superior_derecha": ["superior_izquierda", "inferior_derecha"],
            "inferior_izquierda": ["inferior_derecha", "superior_izquierda"],
            "inferior_derecha": ["inferior_izquierda", "superior_derecha"]
        }
        return other_region in adyacentes[self.region]

    def alert_pacman_position(self, pacman_pos):
        self.pacman_knowledge["position"] = pacman_pos
        self.pacman_knowledge["iterations"] = 8
        self.alerted = True
        print(f"{self.name} ha sido alertado de la posición de Pac-Man en {pacman_pos} y mantendrá esta posición por 8 iteraciones.")

    def is_valid_move_in_region(self, posicion):
        x, y = posicion
        limites = {
            "superior_izquierda": (1, 1, 9, 9),
            "superior_derecha": (10, 1, 18, 9),
            "inferior_izquierda": (1, 10, 9, 18),
            "inferior_derecha": (10, 10, 18, 18)
        }
        xmin, ymin, xmax, ymax = limites[self.region]
        return xmin <= x <= xmax and ymin <= y <= ymax


    def is_in_home_region(self, board):
        home_center = board.get_region_center(self.region)
        return self.coord == home_center

    def move_to_home_region(self, board):
        return self.bfs(board.get_region_center(self.region), board)

    def is_in_opposite_corner(self, pacman_pos):
        px, py = pacman_pos
        gx, gy = self.coord
        return abs(px - gx) + abs(py - gy) > 2
    

    def bfs(self, objetivo, board):
        """BFS para Clyde."""
        visitados = set()
        cola = deque([(self.coord, [])])
        visitados.add(self.coord)

        while cola:
            (x, y), camino = cola.popleft()
            if (x, y) == objetivo:
                return camino[1] if len(camino) > 1 else self.coord
            for nx, ny in board.getAdj(x, y):
                if (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    cola.append(((nx, ny), camino + [(x, y)]))
        return self.coord

    def greedy_bfs(self, objetivo, board):
        """Greedy BFS para Blinky."""
        visitados = set()
        cola = []
        heapq.heappush(cola, (self.heuristica(self.coord, objetivo), self.coord, []))

        while cola:
            _, actual, camino = heapq.heappop(cola)
            if actual == objetivo:
                return camino[1] if len(camino) > 1 else actual
            if actual not in visitados:
                visitados.add(actual)
                for vecino in board.getAdj(actual[0], actual[1]):
                    if vecino not in visitados:
                        nuevo_camino = camino + [actual]
                        heapq.heappush(cola, (self.heuristica(vecino, objetivo), vecino, nuevo_camino))
        return self.coord


    def bidirectional_search(self, objetivo, board):
        """Búsqueda bidireccional para Pinky, retorna solo el primer paso hacia el objetivo."""
        visitados_inicial, visitados_objetivo = set(), set()
        cola_inicial, cola_objetivo = deque([(self.coord, [])]), deque([(objetivo, [])])
        caminos_inicial, caminos_objetivo = {self.coord: []}, {objetivo: []}

        while cola_inicial and cola_objetivo:
            # Búsqueda desde el inicio
            actual_inicio, camino_inicio = cola_inicial.popleft()
            if actual_inicio in visitados_objetivo:
                camino_objetivo = caminos_objetivo[actual_inicio]
                camino_total = camino_inicio + camino_objetivo[::-1]
                # Retorna solo el primer paso hacia el objetivo
                return camino_total[1] if len(camino_total) > 1 else actual_inicio

            visitados_inicial.add(actual_inicio)
            for vecino in board.getAdj(actual_inicio[0], actual_inicio[1]):
                if vecino not in visitados_inicial and vecino not in caminos_inicial:
                    caminos_inicial[vecino] = camino_inicio + [actual_inicio]
                    cola_inicial.append((vecino, caminos_inicial[vecino]))

            # Búsqueda desde el objetivo
            actual_objetivo, camino_objetivo = cola_objetivo.popleft()
            if actual_objetivo in visitados_inicial:
                camino_inicio = caminos_inicial[actual_objetivo]
                camino_total = camino_inicio + camino_objetivo[::-1]
                # Retorna solo el primer paso hacia el objetivo
                return camino_total[1] if len(camino_total) > 1 else actual_objetivo

            visitados_objetivo.add(actual_objetivo)
            for vecino in board.getAdj(actual_objetivo[0], actual_objetivo[1]):
                if vecino not in visitados_objetivo and vecino not in caminos_objetivo:
                    caminos_objetivo[vecino] = camino_objetivo + [actual_objetivo]
                    cola_objetivo.append((vecino, caminos_objetivo[vecino]))

        return self.coord



    def a_star(self, objetivo, board):
        """A* sin colaboración para Inky."""
        visitados = set()
        cola = []
        heapq.heappush(cola, (self.heuristica(self.coord, objetivo), self.coord, []))

        while cola:
            _, actual, camino = heapq.heappop(cola)
            if actual == objetivo:
                return camino[1] if len(camino) > 1 else actual
            if actual not in visitados:
                visitados.add(actual)
                for vecino in board.getAdj(actual[0], actual[1]):
                    if vecino not in visitados:
                        nuevo_camino = camino + [actual]
                        heapq.heappush(cola, (self.heuristica(vecino, objetivo), vecino, nuevo_camino))
        return self.coord



class Pacman(Entities):
    def __init__(self, coord):
        color = "\033[33m██\033[0m"
        is_player = True
        super().__init__(color, coord, is_player)
        
    def update(self, board):
        direccion = input("w,a,s,d para mover a Pac-Man: ")
        self.mover(board.tablero, direccion)
        
    def mover(self, matriz, direccion):
        x, y = self.coord
        nueva_coord = (0, 0)
        
        match direccion:
            case 'w': nueva_coord = (x, y - 1)
            case 's': nueva_coord = (x, y + 1)
            case 'a': nueva_coord = (x - 1, y)
            case 'd': nueva_coord = (x + 1, y)
            case _: nueva_coord = (x, y)
        
        q, w = nueva_coord
        if matriz[w][q] == 1:
            self.coord = nueva_coord