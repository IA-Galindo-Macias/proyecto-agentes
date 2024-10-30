from board import board 
from Entities import Pacman, Fantasma

game = board()

BLINKY_COLOR = "\033[31m██\033[0m"

game.entities.append(Pacman((10,10)))
game.entities.append(Fantasma(BLINKY_COLOR,(1,1)))

while True:
    game.draw()
    game.update()