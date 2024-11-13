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
    def __init__(self, name, color, coord, vision):
        super().__init__(color, coord)
        self.name = name
        self.patrol_point = coord
        self.vision = vision
        

    def move(self, objetivo, board, other_ghosts=None):
        """Movimiento basado en patrulla dinámica con manejo de colisiones."""
        # Si Pacman está lejos, moverse hacia el punto de patrulla
        if self.heuristica(self.coord, objetivo) > self.vision:
            objetivo_real = self.patrol_point
        else:
            objetivo_real = objetivo    # Perseguir a Pacman si está cerca

        nueva_pos = self.bfs(objetivo_real, board)  # Calcular el siguiente movimiento usando BFS

        # Si el objetivo es la patrulla y está a menos de 2 nodos, reasignar un nuevo punto
        if objetivo_real == self.patrol_point and self.heuristica(self.coord, objetivo_real) < 3:
            posibles_puntos = list(board.getGrafo().keys())
            posibles_puntos.remove(self.coord)  # Evitar seleccionar el punto actual
            self.patrol_point = random.choice(posibles_puntos)

        # Verifica si la nueva posición está ocupada por otro fantasma
        if other_ghosts and any(ghost.coord == nueva_pos for ghost in other_ghosts):
            # Cambiar el punto de patrulla si hay colisión
            posibles_puntos = list(board.getGrafo().keys())
            posibles_puntos.remove(self.coord)  # Evitar seleccionar el punto actual
            self.patrol_point = random.choice(posibles_puntos)
            nueva_pos = self.coord  # Quedarse en su posición actual para el siguiente movimiento

        print(self.name,self.coord, nueva_pos, "Patrullando")
        # Actualiza la posición del fantasma
        self.coord = nueva_pos


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
