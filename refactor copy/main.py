from Entities import Pacman, Fantasma, Dot, SuperDot
from board import board

def main():
    game = board()

    pacman = Pacman((1, 1))  
    blinky = Fantasma("BLINKY", "\033[31m██\033[0m", (17, 1), 3)
    pinky = Fantasma("PINKY", "\033[35m██\033[0m", (17, 17), -3)
    inky = Fantasma("INKY", "\033[36m██\033[0m", (9, 11), 3)
    clyde = Fantasma("CLYDE", "\033[38;5;214m██\033[0m", (1, 17), 2)

    game.entities.extend([pacman, blinky, pinky, inky, clyde])
    
    # Agrega Super Dots en posiciones específicas (por ejemplo, algunos puntos en el tablero)
    super_dot_coords = [(1, 9), (9, 9), (17, 9), (7, 5), (11, 13)]  # Coordenadas para Super Dots

    # Verificar que la coordenada esté en un camino y no haya un Dot en la misma posición
    for coord in super_dot_coords:
        x, y = coord
        if game.tablero[x][y] == 1:  # Asegura que solo se coloque en caminos
            # Verificar si ya existe un Dot en esa posición
            if not any(isinstance(entity, Dot) and entity.coord == coord for entity in game.entities):
                game.entities.append(SuperDot(coord))
        else:
            print(f"Coordenada {coord} no es válida para Super Dot (es pared).")

    # Agrega un Dot en cada nodo accesible del tablero
    for coord in game.getGrafo().keys():
        # Solo agrega Dot si no hay un Super Dot en la misma posición
        if not any(isinstance(entity, SuperDot) and entity.coord == coord for entity in game.entities):
            game.entities.append(Dot(coord))



    while True:
        #game.limpiar_terminal()

        game.draw()

        for ghost in [blinky, pinky, inky, clyde]:
            other_ghosts = [g for g in [blinky, pinky, inky, clyde] if g != ghost]
            ghost.move(pacman.coord, game, other_ghosts)

        game.update()


if __name__ == "__main__":
    main()

