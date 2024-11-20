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
    class Estado(Enum):
        PATRULLANDO = 1
        PERSIGUIENDO = 2
        ALERTA = 3
        HUYENDO = 4

    def __init__(self, name, color, coord, vision):
        super().__init__(color, coord)
        self.name = name
        self.patrol_point = coord
        self.base_vision = vision  # Visión base inicial
        self.vision = vision
        self.state = Fantasma.Estado.PATRULLANDO  # Estado inicial
        self.timer_HUYENDO = 0  # Temporizador para el estado HUYENDO

    def move(self, pacman_coord, board, other_ghosts=None):
        """Define movement based on the current state."""
        # Buscar el objeto completo de Pac-Man usando las coordenadas proporcionadas
        pacman = next(
            (entity for entity in board.entities if isinstance(entity, Pacman) and entity.coord == pacman_coord),
            None
        )
        if pacman is None:
            raise ValueError(f"No se encontró el objeto Pac-Man en la posición {pacman_coord}")

        self.update_state(pacman, other_ghosts, board)

        # Define el objetivo real basado en el estado
        if self.state == Fantasma.Estado.PATRULLANDO:
            objetivo_real = self.patrol_point
        elif self.state == Fantasma.Estado.PERSIGUIENDO:
            objetivo_real = pacman.coord
        elif self.state == Fantasma.Estado.ALERTA:
            objetivo_real = self.patrol_point  # Patrulla con visión aumentada
        elif self.state == Fantasma.Estado.HUYENDO:
            self.alejarse_de_pacman(pacman.coord, board)
            return

        nueva_pos = self.bfs(objetivo_real, board)

        # Cambiar el punto de patrulla al llegar al actual
        if self.state == Fantasma.Estado.PATRULLANDO and self.heuristica(self.coord, self.patrol_point) < 3:
            posibles_puntos = list(board.getGrafo().keys())
            posibles_puntos.remove(self.coord)
            self.patrol_point = random.choice(posibles_puntos)

        # Evitar colisiones con otros fantasmas
        if other_ghosts and any(ghost.coord == nueva_pos for ghost in other_ghosts):
            nueva_pos = self.coord

        estado = self.state.name
        print(f"{self.name} ({estado}) - {self.timer_HUYENDO} turnos restantes: "
              f"({self.coord[0]}, {self.coord[1]}) -> ({nueva_pos[0]}, {nueva_pos[1]})")
        self.coord = nueva_pos

    def update_state(self, pacman, other_ghosts, board):
        """Update the state based on the current situation."""
        if self.state == Fantasma.Estado.HUYENDO:
            if self.timer_HUYENDO > 0:
                self.timer_HUYENDO -= 1
                if self.timer_HUYENDO == 0:
                    self.state = Fantasma.Estado.PATRULLANDO
                    print(f"{self.name} salió del estado HUYENDO")
        else:
            if pacman.super_power_active and self.heuristica(self.coord, pacman.coord) <= 3:
                self.state = Fantasma.Estado.HUYENDO
                self.change_state_to_huida()
            elif self.heuristica(self.coord, pacman.coord) <= self.vision:
                self.state = Fantasma.Estado.PERSIGUIENDO
                self.vision = self.base_vision
            elif any(
                ghost.state == Fantasma.Estado.PERSIGUIENDO and
                self.heuristica(ghost.coord, self.coord) <= 3
                for ghost in other_ghosts
            ):
                self.state = Fantasma.Estado.ALERTA
                self.vision = self.base_vision + 3
            else:
                self.state = Fantasma.Estado.PATRULLANDO
                self.vision = self.base_vision

    def change_state_to_huida(self):
        """Cambia el estado del fantasma a HUYENDO."""
        self.state = Fantasma.Estado.HUYENDO
        self.timer_HUYENDO = 10  # Duración de la huida (10 turnos)
        print(f"{self.name} cambió a estado HUYENDO.")

    def bfs(self, objetivo, board):
        """Búsqueda en amplitud para encontrar el siguiente movimiento."""
        visitados = set()
        cola = deque([(self.coord, [])])
        visitados.add(self.coord)

        while cola:
            (x, y), camino = cola.popleft()
            if (x, y) == objetivo:
                return camino[0] if camino else (x, y)
            for nx, ny in board.getAdj(x, y):
                if (nx, ny) not in visitados and board.tablero[ny][nx] == 1:  # Verifica si es camino libre
                    visitados.add((nx, ny))
                    cola.append(((nx, ny), camino + [(nx, ny)]))
        return self.coord  # Si no se encuentra un camino, regresa la posición actual

    def alejarse_de_pacman(self, pacman_coord, board):
        """Se aleja lo más posible de Pac-Man."""
        posibles_movimientos = board.getAdj(*self.coord)
        mejor_movimiento = self.coord
        max_distancia = 3

        for movimiento in posibles_movimientos:
            distancia = self.heuristica(movimiento, pacman_coord)
            if distancia > max_distancia:
                mejor_movimiento = movimiento
                max_distancia = distancia

        print(f"{self.name} (HUYENDO) - {self.timer_HUYENDO} turnos restantes: "
              f"({self.coord[0]}, {self.coord[1]}) -> ({mejor_movimiento[0]}, {mejor_movimiento[1]})")
        self.coord = mejor_movimiento


class Pacman(Entities):
    def __init__(self, coord):
        color = "\033[33m██\033[0m"
        is_player = True
        super().__init__(color, coord, is_player)
        
        # Initialize super power attributes
        self.super_power_active = False
        self.super_power_timer = 0

    def update(self, board, fantasmas):
        direccion = input("w,a,s,d para mover a Pac-Man: ")
        self.mover(board.tablero, direccion)

        # Verifica si Pac-Man consumió un Super DOT
        entidad_en_coord = board.buscar_coord(self.coord)
        if entidad_en_coord and isinstance(entidad_en_coord, SuperDot):
            board.tablero[self.coord[0]][self.coord[1]] = ' '  # Limpia el Super Dot del tablero
            self.activate_super_power(fantasmas)  # Activa el poder de Super Dot
        
        # Si el poder está activo, el temporizador va decrementando
        if self.super_power_active:
            self.super_power_timer -= 1
            if self.super_power_timer <= 0:
                self.deactivate_super_power()  # Desactiva el poder después de un tiempo

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

    def activate_super_power(self, fantasmas):
        """Activa el poder de Super Dot."""
        print("¡Poder de Super Dot activado!")
        self.super_power_active = True
        self.super_power_timer = 5  # Duración del poder en turnos
        for fantasma in fantasmas:
            fantasma.change_state_to_huida()  # Los fantasmas huyen durante el poder

    def deactivate_super_power(self):
        """Desactiva el poder de Super Dot."""
        print("¡Poder de Super Dot desactivado!")
        self.super_power_active = False


class Dot(Entities):
    def __init__(self, coord):
        super().__init__(" .", coord)
    
    def update(self, board):
        pass

class SuperDot(Entities):
    def __init__(self, coord):
        super().__init__(" \033[1;37mS\033[0m", coord)  # Añadido el color al constructor
        self.symbol = "S"

    def draw(self):
        # Dibuja el Super Dot con un color distinto
        print(self.color, end="")

