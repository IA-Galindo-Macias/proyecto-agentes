class Entities:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        
    def update(self, matriz, lista):
        pass
    
    def draw(self):
        pass
    
    
class Pacman(Entities):
    
    def __init__(self, coord):
        color = "\033[33m██\033[0m"
        super().__init__(color, coord)
        
    def update(self, matriz, lista):
        direccion = input("w,a,s,d para mover a Pac-Man: ")
        self.mover(matriz, direccion)
        
    def draw(self):
        print(self.color, end="")
        
    def mover(self,matriz, direccion):
        x, y = self.coord
        nueva_coord = (0,0)
        
        match direccion:
            case 'w': nueva_coord = (x, y - 1)
            case 's': nueva_coord = (x, y + 1)
            case 'a': nueva_coord = (x - 1, y)
            case 'd': nueva_coord = (x + 1, y)
            case _: nueva_coord = (x, y)
            
        self.coord = nueva_coord
            