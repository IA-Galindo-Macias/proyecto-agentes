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
        print()  # Nueva línea al final de cada fila

# Tablero definido como una lista de listas (0: pared, 1: camino)
tablero = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Posiciones iniciales de Pac-Man y los fantasmas
pacman_pos = (1, 9)
blinky_pos = (9, 1)
pinky_pos = (9, 17)
inky_pos = (5, 9)
clyde_pos = (8, 9)

def posicion_valida(tablero, pos):
    x, y = pos
    return 0 <= x < len(tablero) and 0 <= y < len(tablero[0]) and tablero[x][y] == 1

def verificar_colision(pacman_pos, fantasmas_pos):
    for fantasma_pos in fantasmas_pos:
        if pacman_pos == fantasma_pos:
            print("¡Colisión! Pac-Man ha sido atrapado.")
            return True
    return False

# Función para mover Pac-Man
def mover_pacman(tablero, pacman_pos, direccion):
    x, y = pacman_pos
    if direccion == 'w' and x > 0 and tablero[x-1][y] == 1:  # arriba
        return (x-1, y)
    elif direccion == 's' and x < len(tablero)-1 and tablero[x+1][y] == 1:  # abajo
        return (x+1, y)
    elif direccion == 'a' and y > 0 and tablero[x][y-1] == 1:  # izquierda
        return (x, y-1)
    elif direccion == 'd' and y < len(tablero[0])-1 and tablero[x][y+1] == 1:  # derecha
        return (x, y+1)
    return pacman_pos  # No se mueve si no hay camino

def mover_fantasma(fantasma_pos, nueva_pos, tablero):
    # Verificar si la nueva posición es válida
    if posicion_valida(tablero, nueva_pos):
        return nueva_pos
    else:
        return fantasma_pos  # Si no es transitable, se queda en su posición

def mover_blinky(tablero, blinky_pos, pacman_pos):
    nuevo_pos = greedy_bfs(tablero, blinky_pos, pacman_pos)
    return mover_fantasma(blinky_pos, nuevo_pos, tablero)

def mover_pinky(tablero, pinky_pos, pacman_pos):
    nuevo_pos = bidirectional_search(tablero, pinky_pos, pacman_pos)
    return mover_fantasma(pinky_pos, nuevo_pos, tablero)

def mover_inky(tablero, inky_pos, blinky_pos, pacman_pos):
    nuevo_pos = a_star_with_collab(tablero, inky_pos, pacman_pos, blinky_pos)
    return mover_fantasma(inky_pos, nuevo_pos, tablero)

def mover_clyde(tablero, clyde_pos, pacman_pos):
    adyacentes = getAdj(tablero, clyde_pos[0], clyde_pos[1])
    return random.choice(adyacentes) if adyacentes else clyde_pos

def imprimir_estado(tablero, blinky_pos, pinky_pos, inky_pos, pacman_pos, clyde_pos):
    print(f"Blinky: {blinky_pos}, Pinky: {pinky_pos}, Inky: {inky_pos}, Clyde: {clyde_pos}, Pac-Man: {pacman_pos}")

# Bucle principal del juego
while True:
    #limpiar_terminal()
    imprimir_tablero_con_fantasmas(tablero, pacman_pos, blinky_pos, pinky_pos, inky_pos, clyde_pos)

    # Input del jugador para mover a Pac-Man
    direccion = input("w,a,s,d para mover a Pac-Man: ")
    pacman_pos = mover_pacman(tablero, pacman_pos, direccion)

    # Mover los fantasmas
    blinky_pos = mover_blinky(tablero, blinky_pos, pacman_pos)
    pinky_pos = mover_pinky(tablero, pinky_pos, pacman_pos)
    inky_pos = mover_inky(tablero, inky_pos, blinky_pos, pacman_pos)
    clyde_pos = mover_clyde(tablero, clyde_pos, pacman_pos)

    imprimir_estado(tablero, blinky_pos, pinky_pos, inky_pos, pacman_pos, clyde_pos)

    # Verificar colisión entre Pac-Man y los fantasmas
    if verificar_colision(pacman_pos, [blinky_pos, pinky_pos, inky_pos, clyde_pos]):
        break
    print("---------------------------------------------------------------")
