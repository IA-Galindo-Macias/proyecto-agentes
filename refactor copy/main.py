from Entities import Pacman, Fantasma
from board import board

def main():
    game = board()

    pacman = Pacman((1, 1))  
    blinky = Fantasma("BLINKY", "\033[31m██\033[0m", (17, 1), 3)
    pinky = Fantasma("PINKY", "\033[35m██\033[0m", (17, 17), 3)
    inky = Fantasma("INKY", "\033[36m██\033[0m", (9, 11), 3)
    clyde = Fantasma("CLYDE", "\033[38;5;214m██\033[0m", (1, 17),2 )

    game.entities.extend([pacman, blinky, pinky, inky, clyde])

    while True:
        game.limpiar_terminal()

        game.draw()

        for ghost in [blinky, pinky, inky, clyde]:
            other_ghosts = [g for g in [blinky, pinky, inky, clyde] if g != ghost]
            ghost.move(pacman.coord, game, other_ghosts)

        game.update()


if __name__ == "__main__":
    main()

