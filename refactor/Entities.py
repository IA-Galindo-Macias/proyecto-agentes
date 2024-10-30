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

def heuristica(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def greedy_bfs_grafo(grafo, inicio, objetivo):
    visitados = set()
    cola = []
    heapq.heappush(cola, (heuristica(inicio, objetivo), inicio, []))

    while cola:
        _, actual, camino = heapq.heappop(cola)
        if actual == objetivo:
            return camino[1] if len(camino) > 1 else actual
        if actual not in visitados:
            visitados.add(actual)
            for vecino in grafo.get(actual, []):
                if vecino not in visitados:
                    nuevo_camino = camino + [actual]
                    heapq.heappush(cola, (heuristica(vecino, objetivo), vecino, nuevo_camino))
    
    return inicio


class Fantasma(Entities):
    
    def update(self, board):
        ent = [entity for entity in board.entities if entity.player]
        nuevo_pos = greedy_bfs_grafo(board.grafo_adyacencias, self.coord, ent[0].coord)    
        
        self.coord = self.mover_fantasma(nuevo_pos, board.grafo_adyacencias)
    
    def mover_fantasma(self, nueva_pos, grafo):
        if nueva_pos in grafo:
            return nueva_pos
        else:
            return self.coord

    
class Pacman(Entities):
    
    def __init__(self, coord):
        color = "\033[33m██\033[0m"
        is_player = True
        super().__init__(color, coord, is_player)
        
    def update(self, board):
        direccion = input("w,a,s,d para mover a Pac-Man: ")
        self.mover(board.tablero, direccion)
        
    def mover(self,matriz, direccion):
        x, y = self.coord
        nueva_coord = (0,0)
        
        match direccion:
            case 'w': nueva_coord = (x, y - 1)
            case 's': nueva_coord = (x, y + 1)
            case 'a': nueva_coord = (x - 1, y)
            case 'd': nueva_coord = (x + 1, y)
            case _: nueva_coord = (x, y)
        
        q,w = nueva_coord
        if matriz[w][q] == 1:
            self.coord = nueva_coord
            
            
            