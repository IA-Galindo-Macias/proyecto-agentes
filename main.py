from collections import deque

# Función para obtener las celdas adyacentes que tienen valor 1
def getAdj(tablero, x, y):
    adjacentes = []
    filas = len(tablero)
    columnas = len(tablero[0])

    # Verificar las celdas adyacentes (izquierda, derecha, arriba, abajo)
    if y - 1 >= 0 and tablero[x][y-1] == 1:
        adjacentes.append((x, y-1))
    if y + 1 < columnas and tablero[x][y+1] == 1:
        adjacentes.append((x, y+1))
    if x - 1 >= 0 and tablero[x-1][y] == 1:
        adjacentes.append((x-1, y))
    if x + 1 < filas and tablero[x+1][y] == 1:
        adjacentes.append((x+1, y))

    return adjacentes

# Función para generar la lista de adyacencias, solo considerando celdas con valor 1
def generar_lista_adyacencias(tablero):
    lista_adyacencias = {}
    filas = len(tablero)
    columnas = len(tablero[0])

    # Recorremos cada celda del tablero
    for x in range(filas):
        for y in range(columnas):
            # Solo procesamos las celdas con valor 1
            if tablero[x][y] == 1:
                adyacentes = getAdj(tablero, x, y)
                if adyacentes:  # Solo agregar si hay adyacencias
                    lista_adyacencias[(x, y)] = adyacentes
    
    return lista_adyacencias

# Función de Búsqueda en Anchura (BFS) para encontrar el camino más corto entre dos nodos
def bfs_caminos(tablero, inicio, objetivo):
    # Generar el grafo de adyacencias a partir del tablero
    grafo = generar_lista_adyacencias(tablero)
    
    # Inicializar la cola de BFS y el diccionario de predecesores
    cola = deque([inicio])
    predecesores = {inicio: None}  # Guarda de dónde viene cada nodo

    # Explorar el grafo utilizando BFS
    while cola:
        nodo_actual = cola.popleft()
        
        # Si encontramos el objetivo, reconstruimos el camino
        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = predecesores[nodo_actual]
            return camino[::-1]  # Devolvemos el camino en el orden correcto
        
        # Explorar los nodos vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in predecesores:  # Solo explorar nodos no visitados
                predecesores[vecino] = nodo_actual
                cola.append(vecino)
    
    # Si no se encuentra un camino, devolvemos None
    return None

# Tablero de ejemplo con celdas con valor 1 que representan los nodos del grafo
tablero = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
]

# Definir los nodos de inicio y objetivo para buscar el camino más corto
inicio = (0, 0)
objetivo = (9, 9)

# Encontrar el camino más corto utilizando BFS
camino_mas_corto = bfs_caminos(tablero, inicio, objetivo)

# Imprimir el resultado del camino más corto
print("Camino más corto:", camino_mas_corto)
