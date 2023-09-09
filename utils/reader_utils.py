from utils.custom_exceptions import NotEqualMatrixError
import random

def read_input(path:str):
    x_len = None
    raw_matrix = []
    with open(path) as f:
        for idx, line in enumerate(f.readlines()):
            curr_line = line.replace('\n','')
            if idx == 0:
                x_len = len(curr_line)
            if len(curr_line) != x_len:
                raise NotEqualMatrixError("Please Input an NxN matrix")
            else:
                raw_matrix.append(curr_line)
    return raw_matrix
    
def txt_to_grid(map: list):
    grid = []
    for y,row in enumerate(map):
        grid_row = []
        for x,occupant in enumerate(row):
            grid_row.append(Occupant(occupant,(x,y)))
        grid.append(grid_row)
    return grid

class Occupant:
    def __init__(self, 
                 race: str, 
                 location: tuple):
        self.race = race
        self.location = location
        
class GridMap:
    def __init__(self, 
                 map: list):
        self.map = txt_to_grid(map)
        self.shape = (len(self.map[0]),len(self.map)) # (x-size, y-size)
        self.population = self._count_race()
        
    def print_grid(self,map=None):
        if map is None:
            map = self.map
        for row in map:
            print(" ".join([occupant.race for occupant in row]))
            
    def _count_race(self,map=None):
        if map is None:
            map = self.map
        population = {}
        for row in map:
            for occupant in row:
                if occupant.race != " ":
                    try:
                        population[occupant.race] += 1
                    except Exception as e:
                        population[occupant.race] = 1
        return population
    
    def _get_random_subregion(self, subregion_size):
        rand_x = (random.randint(0,self.shape[0]-subregion_size))
        rand_y = (random.randint(0,self.shape[1]-subregion_size))
        sub_region = self.map[rand_y:rand_y+subregion_size]
        for idx,row in enumerate(sub_region):
            sub_region[idx] = row[rand_x:rand_x+subregion_size]
        return sub_region
    
    def get_dissimilarity_index(self, 
                                subregion: str = None,
                                subregion_size: int = 4
                                ) -> str:
        if subregion is None:
            sub_region = self._get_random_subregion(subregion_size)
        
        print("SUB REGION:")
        self.print_grid(sub_region)
        sub_region_population = self._count_race(sub_region)
        
        print(f"SUB REGION POPULATION: {sub_region_population}")
        races = list(self.population.keys())
        val1 = sub_region_population[races[0]]/self.population[races[0]]
        val2 = sub_region_population[races[1]]/self.population[races[1]]
        dissimilarity_index = abs(val1-val2)
        
        print(f"DISSIMILARITY INDEX: {dissimilarity_index} or {dissimilarity_index:.3f}")
    
    def simulate_segregation(self,
                             type:str="default",
                             satisfaction:float=.5
                            ) -> str:
        
        return 0
        
    

