from Entities import Pacman, Fantasma
from board import board

def main():
    game = board()

    pacman = Pacman((9, 11))
    blinky = Fantasma("BLINKY", "\033[31m██\033[0m", (17, 1), "superior_derecha")
    pinky = Fantasma("PINKY", "\033[35m██\033[0m", (17, 17), "inferior_derecha")
    inky = Fantasma("INKY", "\033[36m██\033[0m", (1, 17), "inferior_izquierda")
    clyde = Fantasma("CLYDE", "\033[38;5;214m██\033[0m", (1, 1), "superior_izquierda")

    game.entities.extend([pacman, blinky, pinky, inky, clyde])

    while True:
        game.draw()
        game.update()

if __name__ == "__main__":
    main()
