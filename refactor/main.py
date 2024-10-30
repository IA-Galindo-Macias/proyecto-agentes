from board import board 
from Entities import Pacman

game = board()

game.entities.append(Pacman((1,1)))

while True:
    game.draw()
    game.update()