import os
from preboard import *


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
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    
        self.grafo_adyacencias = generar_lista_adyacencias(self.tablero)

        self.entities = []



    def limpiar_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def imprimir_tablero_con_fantasmas(tablero, pacman_pos, blinky_pos, pinky_pos, inky_pos, clyde_pos):
        PACMAN_COLOR = "\033[33m██\033[0m"  # Pac-Man es amarillo
        BLINKY_COLOR = "\033[31m██\033[0m"  # Blinky es rojo
        PINKY_COLOR = "\033[35m██\033[0m"   # Pinky es magenta
        INKY_COLOR = "\033[36m██\033[0m"    # Inky es azul
        CLYDE_COLOR = "\033[38;5;214m██\033[0m"  # Clyde es naranja
        PARED = "\033[34m██\033[0m"  # Pared azul
        CAMINO = "\033[40m  \033[0m"  # Fondo negro

        for i, fila in enumerate(tablero):
            for j, celda in enumerate(fila):
                if (i, j) == pacman_pos:
                    print(PACMAN_COLOR, end="")
                elif (i, j) == blinky_pos:
                    print(BLINKY_COLOR, end="")
                elif (i, j) == pinky_pos:
                    print(PINKY_COLOR, end="")
                elif (i, j) == inky_pos:
                    print(INKY_COLOR, end="")
                elif (i, j) == clyde_pos:
                    print(CLYDE_COLOR, end="")
                elif celda == 0:
                    print(PARED, end="")
                else:
                    print(CAMINO, end="")
            print()



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

    def update(self, tablero, pacman_pos, blinky_pos, pinky_pos, inky_pos, clyde_pos):
        self.imprimir_tablero_con_fantasmas(tablero, pacman_pos, blinky_pos, pinky_pos, inky_pos, clyde_pos)