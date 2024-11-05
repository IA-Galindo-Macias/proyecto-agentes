from collections import deque
import heapq
import random

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
        """Heurística Manhattan para calcular distancia."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Fantasma(Entities):
    def __init__(self, name, color, coord):
        super().__init__(color, coord)
        self.name = name

    def move(self, objetivo, board, blinky_pos=None, other_ghosts=None):
        """Método de movimiento personalizado según el tipo de fantasma."""
        nueva_pos = self.coord  # Posición por defecto es la posición actual
        if self.name == "BLINKY":
            nueva_pos = self.greedy_bfs(objetivo, board)
        elif self.name == "PINKY":
            nueva_pos = self.bidirectional_search(objetivo, board)
        elif self.name == "INKY":
            nueva_pos = self.a_star_with_collab(objetivo, blinky_pos, board)
        elif self.name == "CLYDE":
            nueva_pos = self.bfs(objetivo, board)
        
        # Verifica que la nueva posición no esté ocupada por otros fantasmas
        if other_ghosts and any(ghost.coord == nueva_pos for ghost in other_ghosts):
            nueva_pos = self.coord  # Si está ocupada, permanece en la posición actual

        # Actualiza la posición del fantasma
        self.coord = nueva_pos



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
        """Búsqueda bidireccional para Pinky."""
        visitados_inicial, visitados_objetivo = set(), set()
        cola_inicial, cola_objetivo = deque([(self.coord, [])]), deque([(objetivo, [])])
        caminos_inicial, caminos_objetivo = {self.coord: []}, {objetivo: []}

        while cola_inicial and cola_objetivo:
            # Búsqueda desde el inicio
            actual_inicio, camino_inicio = cola_inicial.popleft()
            if actual_inicio in visitados_objetivo:
                camino_objetivo = caminos_objetivo[actual_inicio]
                camino_total = camino_inicio + camino_objetivo[::-1]
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
                return camino_total[1] if len(camino_total) > 1 else actual_objetivo
            visitados_objetivo.add(actual_objetivo)
            for vecino in board.getAdj(actual_objetivo[0], actual_objetivo[1]):
                if vecino not in visitados_objetivo and vecino not in caminos_objetivo:
                    caminos_objetivo[vecino] = camino_objetivo + [actual_objetivo]
                    cola_objetivo.append((vecino, caminos_objetivo[vecino]))
        return self.coord

    def a_star_with_collab(self, objetivo, blinky_pos, board):
        """A* con colaboración para Inky."""
        visitados = set()
        cola = []
        heapq.heappush(cola, (self.heuristica(self.coord, objetivo), self.coord, []))

        while cola:
            _, actual, camino = heapq.heappop(cola)
            if actual == objetivo or (blinky_pos and self.heuristica(actual, blinky_pos) > 6):
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
