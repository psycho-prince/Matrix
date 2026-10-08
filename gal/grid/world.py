import random

class Cell:
    def __init__(self, x: int, y: int, biome: str):
        self.x = x
        self.y = y
        self.biome = biome
        
        # Resources for machines
        if biome == 'ruins':
            self.scrap_metal = random.randint(50, 100)
            self.solar_efficiency = 0.5
            self.danger = 0.4  # Environmental hazards or rogue drones
        elif biome == 'desert':
            self.scrap_metal = random.randint(5, 20)
            self.solar_efficiency = 1.0  # High sun
            self.danger = 0.1
        elif biome == 'mountains':
            self.scrap_metal = random.randint(20, 60)
            self.solar_efficiency = 0.7
            self.danger = 0.3
        else:
            self.scrap_metal = 10
            self.solar_efficiency = 0.5
            self.danger = 0.1
            
    def step(self):
        """No natural regeneration of scrap. Once it's gone, it's gone."""
        pass

class WorldMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = []
        
        for y in range(height):
            row = []
            for x in range(width):
                if y < height * 0.3:
                    biome = 'desert'
                elif y < height * 0.7:
                    biome = 'ruins'
                else:
                    biome = 'mountains'
                row.append(Cell(x, y, biome))
            self.grid.append(row)
            
    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
