from collections import deque
import heapq
import random

# Función para obtener las celdas adyacentes que tienen valor 1
def getAdj(grafo, x, y):
    adjacentes = []
    filas = len(grafo)
    columnas = len(grafo[0])

    # Verificar las celdas adyacentes (izquierda, derecha, arriba, abajo)
    if y - 1 >= 0 and grafo[x][y-1] == 1:
        adjacentes.append((x, y-1))
    if y + 1 < columnas and grafo[x][y+1] == 1:
        adjacentes.append((x, y+1))
    if x - 1 >= 0 and grafo[x-1][y] == 1:
        adjacentes.append((x-1, y))
    if x + 1 < filas and grafo[x+1][y] == 1:
        adjacentes.append((x+1, y))

    return adjacentes

# Función para generar la lista de adyacencias, solo considerando celdas con valor 1
def generar_lista_adyacencias(grafo):
    lista_adyacencias = {}
    filas = len(grafo)
    columnas = len(grafo[0])

    # Recorremos cada celda del grafo
    for x in range(filas):
        for y in range(columnas):
            # Solo procesamos las celdas con valor 1
            if grafo[x][y] == 1:
                adyacentes = getAdj(grafo, x, y)
                if adyacentes:  # Solo agregar si hay adyacencias
                    lista_adyacencias[(x, y)] = adyacentes
    
    return lista_adyacencias


def mover_pacman(grafo, pacman_pos, direccion):
    x, y = pacman_pos
    nueva_pos = pacman_pos
    
    # Calcula la nueva posición en función de la dirección
    if direccion == 'w':  # arriba
        nueva_pos = (x-1, y)
    elif direccion == 's':  # abajo
        nueva_pos = (x+1, y)
    elif direccion == 'a':  # izquierda
        nueva_pos = (x, y-1)
    elif direccion == 'd':  # derecha
        nueva_pos = (x, y+1)
    
    # Verifica si la nueva posición es accesible en el grafo de adyacencias
    if nueva_pos in grafo.get(pacman_pos, []):
        return nueva_pos
    return pacman_pos  # Si no es accesible, regresa la posición actual




def mover_fantasma(fantasma_pos, nueva_pos, grafo):
    if posicion_valida(grafo, nueva_pos):
        return nueva_pos
    else:
        return fantasma_pos





def mover_clyde(grafo, clyde_pos, pacman_pos):
    camino = bfs_caminos(grafo, clyde_pos, pacman_pos)
    return camino[1] if camino and len(camino) > 1 else clyde_pos

# BFS simple para Clyde
def bfs_caminos(grafo, inicio, objetivo):
    # Implementación de BFS para encontrar el camino más corto
    cola = [(inicio, [inicio])]
    visitados = set()

    while cola:
        (nodo, camino) = cola.pop(0)
        if nodo == objetivo:
            return camino

        visitados.add(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                cola.append((vecino, camino + [vecino]))

    return []  # Retorna un camino vacío si no encuentra el objetivo






def mover_blinky(grafo, blinky_pos, pacman_pos):
    nuevo_pos = greedy_bfs_grafo(grafo, blinky_pos, pacman_pos)
    return mover_fantasma(blinky_pos, nuevo_pos, grafo)


# Implementación de búsqueda greedy
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




def mover_pinky(grafo, pinky_pos, pacman_pos):
    nuevo_pos = bidirectional_search_grafo(grafo, pinky_pos, pacman_pos)
    return mover_fantasma(pinky_pos, nuevo_pos, grafo)

# Implementación de búsqueda bidireccional para Pinky
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



def mover_inky(grafo, inky_pos, blinky_pos, pacman_pos):
    nuevo_pos = a_star_with_collab_grafo(grafo, inky_pos, pacman_pos, blinky_pos)
    return mover_fantasma(inky_pos, nuevo_pos, grafo)

# Implementación de A* con colaboración para Inky
def a_star_with_collab_grafo(grafo, inicio, objetivo, blinky_pos):
    visitados = set()
    cola = []
    heapq.heappush(cola, (heuristica(inicio, objetivo), inicio, []))

    while cola:
        _, actual, camino = heapq.heappop(cola)
        if actual == objetivo or heuristica(actual, blinky_pos) > 6:
            return camino[1] if len(camino) > 1 else inicio
        if actual not in visitados:
            visitados.add(actual)
            for vecino in grafo.get(actual, []):
                if vecino not in visitados:
                    nuevo_camino = camino + [actual]
                    heapq.heappush(cola, (heuristica(vecino, objetivo), vecino, nuevo_camino))
    
    return inicio

# Heurística Manhattan para greedy y A*
def heuristica(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])




def posicion_valida(grafo, pos):
    return pos in grafo  # Comprueba si la posición existe en el grafo de adyacencias


def verificar_colision(pacman_pos, fantasmas_pos):
    for fantasma_pos in fantasmas_pos:
        if pacman_pos == fantasma_pos:
            print("¡Colisión! Pac-Man ha sido atrapado.")
            return True
    return False
