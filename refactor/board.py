import os

class board:
    def __init__(self):
        self.tablero = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    
        self.grafo_adyacencias = self.generar_lista_adyacencias(self.tablero)

        self.entities = []



    def limpiar_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Función que busca la tupla en la lista de instancias
    def buscar_coord(self, coord):
        for entidad in self.entities:
            if entidad.coord == coord:
                return entidad  # Devuelve la tupla si la encuentra
        return None  # Devuelve None si no existe

    def draw(self):
        PARED = "\033[34m██\033[0m"  # Pared azul
        CAMINO = "\033[40m  \033[0m"  # Fondo negro

        for y, row in enumerate(self.tablero):
            for x, cell in enumerate(row):
                foo = self.buscar_coord((x, y))  # Usa (x, y) como coordenadas

                if foo is not None:
                    foo.draw()

                elif cell == 0:
                    print(PARED, end="")
                else:
                    print(CAMINO, end="")

            print()


            



    def getAdj(self, x, y):
        adjacentes = []
        filas = len(self.tablero)
        columnas = len(self.tablero[0])

        # Verificar las celdas adyacentes (izquierda, derecha, arriba, abajo)
        if y - 1 >= 0 and self.tablero[x][y-1] == 1:
            adjacentes.append((x, y-1))
        if y + 1 < columnas and self.tablero[x][y+1] == 1:
            adjacentes.append((x, y+1))
        if x - 1 >= 0 and self.tablero[x-1][y] == 1:
            adjacentes.append((x-1, y))
        if x + 1 < filas and self.tablero[x+1][y] == 1:
            adjacentes.append((x+1, y))

        return adjacentes

    # Función para generar la lista de adyacencias, solo considerando celdas con valor 1
    def generar_lista_adyacencias(self, grafo):
        lista_adyacencias = {}
        filas = len(grafo)
        columnas = len(grafo[0])

        # Recorremos cada celda del grafo
        for x in range(filas):
            for y in range(columnas):
                # Solo procesamos las celdas con valor 1
                if grafo[x][y] == 1:
                    adyacentes = self.getAdj(x, y)
                    if adyacentes:  # Solo agregar si hay adyacencias
                        lista_adyacencias[(x, y)] = adyacentes
        
        return lista_adyacencias

    
    
    def getGrafo(self):
        return self.grafo_adyacencias
    
    def getTablero(self):
        return self.tablero
    

    def verificar_colision(pacman_pos, fantasmas_pos):
        for fantasma_pos in fantasmas_pos:
            if pacman_pos == fantasma_pos:
                print("¡Colisión! Pac-Man ha sido atrapado.")
                return True
        return False

    def update(self):
        for entidad in self.entities:
            entidad.update(self.tablero, self.grafo_adyacencias)