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

def posicion_valida(grafo, pos):
    return pos in grafo  # Comprueba si la posición existe en el grafo de adyacencias

def heuristica(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def bidirectional_search_grafo(grafo, inicio, objetivo):
    visitados_inicio, visitados_objetivo = set(), set()
    cola_inicio, cola_objetivo = deque([(inicio, [])]), deque([(objetivo, [])])
    caminos_inicio, caminos_objetivo = {inicio: []}, {objetivo: []}

    while cola_inicio and cola_objetivo:
        # Búsqueda desde el inicio
        actual_inicio, camino_inicio = cola_inicio.popleft()
        if actual_inicio in visitados_objetivo:
            camino_objetivo = caminos_objetivo[actual_inicio]
            camino_total = camino_inicio + camino_objetivo[::-1]
            return camino_total[1] if len(camino_total) > 1 else actual_inicio
        visitados_inicio.add(actual_inicio)
        for vecino in grafo.get(actual_inicio, []):
            if vecino not in visitados_inicio and vecino not in caminos_inicio:
                caminos_inicio[vecino] = camino_inicio + [actual_inicio]
                cola_inicio.append((vecino, caminos_inicio[vecino]))

        # Búsqueda desde el objetivo
        actual_objetivo, camino_objetivo = cola_objetivo.popleft()
        if actual_objetivo in visitados_inicio:
            camino_inicio = caminos_inicio[actual_objetivo]
            camino_total = camino_inicio + camino_objetivo[::-1]
            return camino_total[1] if len(camino_total) > 1 else actual_objetivo
        visitados_objetivo.add(actual_objetivo)
        for vecino in grafo.get(actual_objetivo, []):
            if vecino not in visitados_objetivo and vecino not in caminos_objetivo:
                caminos_objetivo[vecino] = camino_objetivo + [actual_objetivo]
                cola_objetivo.append((vecino, caminos_objetivo[vecino]))
    
    return inicio



class Fantasma(Entities):
    
    def update(self, board):
        ent = [entity for entity in board.entities if entity.player]
        nuevo_pos = bidirectional_search_grafo(board.grafo_adyacencias, self.coord, ent[0].coord)
        
        a,b = nuevo_pos
        
        print(nuevo_pos, board.tablero[a][b])
        self.coord = self.mover_fantasma(nuevo_pos, board.grafo_adyacencias)
    
    def mover_fantasma(self, nueva_pos, grafo):
        if posicion_valida(grafo, nueva_pos):
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
            
            
            