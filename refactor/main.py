from board import board 
from Entities import Pacman

game = board()

game.entities.append(Pacman((1,9)))

game.draw()