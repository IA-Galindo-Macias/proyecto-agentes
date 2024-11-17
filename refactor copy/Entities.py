from collections import deque
from enum import Enum
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
    def __init__(self, name, color, coord, vision):
        super().__init__(color, coord)
        self.name = name
        self.patrol_point = coord
        self.vision = vision
        


class Fantasma(Entities):
    class Estado(Enum):
        PATRULLANDO = 1 # No ha visto a pacman
        PERSIGUIENDO = 2 # esta persiguiendo a pacman
        ALERTA = 3 # un fantasma cercano vio a pacman

    def __init__(self, name, color, coord, vision):
        super().__init__(color, coord)
        self.name = name
        self.patrol_point = coord
        self.base_vision = vision  # Vision base inicial
        self.vision = vision
        self.state = Fantasma.Estado.PATRULLANDO  # Estado inicial

    def move(self, objetivo, board, other_ghosts=None):
        """Define movimiento basado en estado."""
        self.update_state(objetivo, other_ghosts, board)
        
        if self.state == Fantasma.Estado.PATRULLANDO:
            objetivo_real = self.patrol_point
        elif self.state == Fantasma.Estado.PERSIGUIENDO:
            objetivo_real = objetivo
        elif self.state == Fantasma.Estado.ALERTA:
            objetivo_real = self.patrol_point  # En alerta, patrulla pero con visión ampliada.

        nueva_pos = self.bfs(objetivo_real, board)

        if objetivo_real == self.patrol_point and self.heuristica(self.coord, objetivo_real) < 3:
            posibles_puntos = list(board.getGrafo().keys())
            posibles_puntos.remove(self.coord)
            self.patrol_point = random.choice(posibles_puntos)

        if other_ghosts and any(ghost.coord == nueva_pos for ghost in other_ghosts):
            posibles_puntos = list(board.getGrafo().keys())
            posibles_puntos.remove(self.coord)
            self.patrol_point = random.choice(posibles_puntos)
            nueva_pos = self.coord

        print(f"{self.name} ({self.state.name}): {self.coord} -> {nueva_pos}")
        self.coord = nueva_pos

    def update_state(self, pacman_coord, other_ghosts, board):
        """Actualiza el estado del fantasma según la situación."""
        if self.heuristica(self.coord, pacman_coord) <= self.vision:
            self.state = Fantasma.Estado.PERSIGUIENDO
            self.vision = self.base_vision  # Reset de visión en persecución
        elif any(ghost.state == Fantasma.Estado.PERSIGUIENDO and self.heuristica(ghost.coord, self.coord) <= 3 for ghost in other_ghosts):
            self.state = Fantasma.Estado.ALERTA
            self.vision = self.base_vision + 3  # Aumenta la visión en estado de alerta
        else:
            self.state = Fantasma.Estado.PATRULLANDO
            self.vision = self.base_vision  # Visión normal al patrullar




    def bfs(self, objetivo, board):
        """BFS para movimiento."""
        visitados = set()
        cola = deque([(self.coord, [])])
        visitados.add(self.coord)

        while cola:
            (x, y), camino = cola.popleft()
            if (x, y) == objetivo:
                # Retorna la próxima posición en el camino o el objetivo si está a un paso
                return camino[0] if camino else (x, y)
            for nx, ny in board.getAdj(x, y):
                if (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    cola.append(((nx, ny), camino + [(nx, ny)]))
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


class Dot(Entities):
    def __init__(self, coord):
        super().__init__(" .", coord)
    
    def update(self, board):
        pass