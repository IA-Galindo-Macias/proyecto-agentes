from collections import deque
import heapq
import random

# Función para obtener posiciones adyacentes
def getAdj(tablero, x, y):
    adyacentes = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(tablero) and 0 <= ny < len(tablero[0]) and tablero[nx][ny] == 1:
            adyacentes.append((nx, ny))
    return adyacentes

# BFS simple para Clyde
def bfs(tablero, inicio, objetivo):
    fila, columna = len(tablero), len(tablero[0])
    visitados = [[False for _ in range(columna)] for _ in range(fila)]
    cola = deque([(inicio, [])])
    visitados[inicio[0]][inicio[1]] = True

    while cola:
        (x, y), camino = cola.popleft()

        if (x, y) == objetivo:
            return camino + [(x, y)]  # Devuelve el camino hasta el objetivo

        for nx, ny in getAdj(tablero, x, y):
            if not visitados[nx][ny]:
                visitados[nx][ny] = True
                cola.append(((nx, ny), camino + [(x, y)]))
    
    return []

# Implementación de búsqueda greedy
def greedy_bfs(tablero, inicio, objetivo):
    visitados = set()
    cola = []
    heapq.heappush(cola, (heuristica(inicio, objetivo), inicio, []))

    while cola:
        _, actual, camino = heapq.heappop(cola)

        if actual == objetivo:
            return camino[1] if len(camino) > 1 else actual  # Moverse al siguiente paso

        if actual not in visitados:
            visitados.add(actual)
            for vecino in getAdj(tablero, actual[0], actual[1]):
                if vecino not in visitados:
                    nuevo_camino = camino + [actual]
                    heapq.heappush(cola, (heuristica(vecino, objetivo), vecino, nuevo_camino))
    
    return inicio  # No se encontró camino, no moverse

# Implementación de búsqueda bidireccional para Pinky
def bidirectional_search(tablero, inicio, objetivo):
    visitados_inicial, visitados_objetivo = set(), set()
    cola_inicial, cola_objetivo = deque([(inicio, [])]), deque([(objetivo, [])])
    
    # Mapa para registrar los caminos desde ambos lados
    caminos_inicial, caminos_objetivo = {inicio: []}, {objetivo: []}

    while cola_inicial and cola_objetivo:
        # Búsqueda desde el inicio
        actual_inicio, camino_inicio = cola_inicial.popleft()
        if actual_inicio in visitados_objetivo:
            # Combinar los caminos desde ambos lados y devolver el primer paso
            camino_objetivo = caminos_objetivo[actual_inicio]
            camino_total = camino_inicio + camino_objetivo[::-1]  # Unir los caminos
            return camino_total[1] if len(camino_total) > 1 else actual_inicio
        visitados_inicial.add(actual_inicio)
        for vecino in getAdj(tablero, actual_inicio[0], actual_inicio[1]):
            if vecino not in visitados_inicial and vecino not in caminos_inicial:
                caminos_inicial[vecino] = camino_inicio + [actual_inicio]
                cola_inicial.append((vecino, caminos_inicial[vecino]))

        # Búsqueda desde el objetivo
        actual_objetivo, camino_objetivo = cola_objetivo.popleft()
        if actual_objetivo in visitados_inicial:
            # Combinar los caminos desde ambos lados y devolver el primer paso
            camino_inicio = caminos_inicial[actual_objetivo]
            camino_total = camino_inicio + camino_objetivo[::-1]
            return camino_total[1] if len(camino_total) > 1 else actual_objetivo
        visitados_objetivo.add(actual_objetivo)
        for vecino in getAdj(tablero, actual_objetivo[0], actual_objetivo[1]):
            if vecino not in visitados_objetivo and vecino not in caminos_objetivo:
                caminos_objetivo[vecino] = camino_objetivo + [actual_objetivo]
                cola_objetivo.append((vecino, caminos_objetivo[vecino]))
    
    return inicio  # No se encontró camino, no moverse


# Implementación de A* con colaboración para Inky
def a_star_with_collab(tablero, inicio, objetivo, blinky_pos):
    visitados = set()
    cola = []
    heapq.heappush(cola, (heuristica(inicio, objetivo), inicio, []))

    while cola:
        _, actual, camino = heapq.heappop(cola)

        if actual == objetivo or heuristica(actual, blinky_pos) > 6:  # Limitar el rango de búsqueda
            # Verificar que el camino tiene pasos
            return camino[1] if len(camino) > 1 else inicio

        if actual not in visitados:
            visitados.add(actual)
            for vecino in getAdj(tablero, actual[0], actual[1]):
                if vecino not in visitados:
                    nuevo_camino = camino + [actual]
                    heapq.heappush(cola, (heuristica(vecino, objetivo), vecino, nuevo_camino))

    return inicio  # No se encontró camino, no moverse



# Heurística Manhattan para greedy y A*
def heuristica(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
