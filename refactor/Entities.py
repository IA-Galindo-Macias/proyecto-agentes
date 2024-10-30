class Entities:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        
    def update(self, matriz):
        pass
    
    def draw(self):
        pass
    
    
class Pacman(Entities):
    
    def __init__(self, coord):
        color = "\033[33m██\033[0m"
        super().__init__(color, coord)
        
    def update(self, matriz, lista):
        direccion = input("w,a,s,d para mover a Pac-Man: ")
        self.mover(matriz, self.coord, direccion)
        
    def draw(self):
        print(self.color, end="")
        
    def mover(self,matriz, pacman_pos, direccion):
        x, y = pacman_pos
        nueva_pos = pacman_pos
        
        # Calcula la nueva posición en función de la dirección
        if direccion == 'w':  # arriba
            nueva_pos = (x-1, y)
        elif direccion == 's':  # abajo
            nueva_pos = (x+1, y)
        elif direccion == 'a':  # izquierda
            nueva_pos = (x, y-1)
        elif direccion == 'd':  # derecha
            nueva_pos = (x, y+1)
        
        if nueva_pos in matriz.get(pacman_pos, []):
            return nueva_pos
        return pacman_pos  # Si no es accesible, regresa la posición actual
            