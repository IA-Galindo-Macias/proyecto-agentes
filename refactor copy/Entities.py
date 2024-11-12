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
        self.patrol_point = coord
        

    def move(self, objetivo, board, other_ghosts=None):
        """Movimiento basado en patrulla dinámica."""
        if self.heuristica(self.coord, objetivo) > 3:
            objetivo = self.patrol_point  # Ir al punto de patrulla si Pacman está lejos
        else:
            objetivo = objetivo  # Si Pacman está cerca, usar lógica de persecución habitual

        nueva_pos = self.bfs(objetivo, board)  # Utilizamos BFS por simplicidad

        # Si llega al punto de patrulla, asigna un nuevo punto aleatorio distinto al actual
        if nueva_pos == self.patrol_point:
            posibles_puntos = list(board.getGrafo().keys())
            posibles_puntos.remove(self.coord)  # Evitar quedarse en el mismo punto
            self.patrol_point = random.choice(posibles_puntos)

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
