import os
from board import *

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

tablero = [
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

# Posiciones iniciales de Pac-Man y los fantasmas
pacman_pos = (1, 9)
blinky_pos = (9, 1)
pinky_pos = (9, 17)
inky_pos = (5, 9)
clyde_pos = (7, 9)



def imprimir_estado(blinky_pos, pinky_pos, inky_pos, pacman_pos, clyde_pos):
    print(f"Blinky: {blinky_pos}, Pinky: {pinky_pos}, Inky: {inky_pos}, Clyde: {clyde_pos}, Pac-Man: {pacman_pos}")

grafo_adyacencias = generar_lista_adyacencias(tablero)

# Bucle principal del juego
while True:
    #limpiar_terminal()
    imprimir_tablero_con_fantasmas(tablero, pacman_pos, blinky_pos, pinky_pos, inky_pos, clyde_pos)
    
    print(grafo_adyacencias)

    direccion = input("w,a,s,d para mover a Pac-Man: ")
    pacman_pos = mover_pacman(grafo_adyacencias, pacman_pos, direccion)

    blinky_pos = mover_blinky(grafo_adyacencias, blinky_pos, pacman_pos)
    print("blinky_pos", greedy_bfs_grafo(grafo_adyacencias, blinky_pos, pacman_pos))

    pinky_pos = mover_pinky(grafo_adyacencias, pinky_pos, pacman_pos)
    inky_pos = mover_inky(grafo_adyacencias, inky_pos, blinky_pos, pacman_pos)
    clyde_pos = mover_clyde(grafo_adyacencias, clyde_pos, pacman_pos)


    imprimir_estado(blinky_pos, pinky_pos, inky_pos, pacman_pos, clyde_pos)

    if verificar_colision(pacman_pos, [blinky_pos, pinky_pos, inky_pos, clyde_pos]):
        break
    print("---------------------------------------------------------------")
