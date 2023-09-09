import random
from utils.custom_exceptions import (NotEqualMatrixError, 
                                     NotInRegionError)

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
        
    def delete(self):
        self.race = " "
    
    def is_empty(self):
        return self.race == " "
        
class GridMap:
    def __init__(self, 
                 map: list):
        self.map = txt_to_grid(map)
        self.shape = (len(self.map[0]),len(self.map)) # (x-size, y-size)
        self.population = self._count_race()
    
    def _grid_to_sep_str(self,map):
        if map is None:
            map = self.map
        combined_str = []
        for row in map:
            combined_str.append(" ".join([occupant.race for occupant in row]))
        return combined_str
            
    def _grid_to_str(self,map):
        if map is None:
            map = self.map
        return "\n".join(self._grid_to_sep_str(map))
    
    def _count_race(self,map=None):
        if map is None:
            map = self.map
        population = {}
        for row in map:
            for occupant in row:
                if not occupant.is_empty():
                    try:
                        population[occupant.race] += 1
                    except Exception as e:
                        population[occupant.race] = 1
        return population

    def _get_random_subregion(self, subregion_size):
        rand_x = (random.randint(0,self.shape[0]-subregion_size))
        rand_y = (random.randint(0,self.shape[1]-subregion_size))
        sub_region = self.map[rand_y:rand_y+subregion_size+1]
        for idx,row in enumerate(sub_region):
            sub_region[idx] = row[rand_x:rand_x+subregion_size+1]
        return sub_region
    
    def copy(self):
        return self.map
        
    def print_grid(self,map=None):
        if map is None:
            map = self.map
        print(self._grid_to_str(map))
    
    def verify_subregion(self, sub_region):
        sub_region_shape = (len(sub_region[0]), len(sub_region))
        stringed_sub_region = self._grid_to_str(sub_region)    
        correct = 0
        for y in range(0,self.shape[1]-sub_region_shape[1]+1):
            for x in range(0,self.shape[0]-sub_region_shape[0]+1):
                chunk = self.map[y:y+sub_region_shape[1]]
                for idx,row in enumerate(chunk):
                    chunk[idx] = row[x:x+sub_region_shape[0]]
                if self._grid_to_str(chunk) == stringed_sub_region:
                    correct+=1
                    break
        return correct
    
    def get_dissimilarity_index(self, 
                                sub_region: str = None,
                                subregion_size: int = 4
                                ) -> str:
        if sub_region is None:
            sub_region = self._get_random_subregion(subregion_size)
        else:
            if not self.verify_subregion(sub_region):
                raise NotInRegionError("Subregion inputted is not in region")
        
        print("SUB REGION:")
        self.print_grid(sub_region)
        sub_region_population = self._count_race(sub_region)
        
        print(f"SUB REGION POPULATION: {sub_region_population}")
        races = list(self.population.keys())
        val1 = sub_region_population[races[0]]/self.population[races[0]]
        val2 = sub_region_population[races[1]]/self.population[races[1]]
        dissimilarity_index = abs(val1-val2)
        
        print(
            f"DISSIMILARITY INDEX: {dissimilarity_index}"
            f" or {dissimilarity_index:.3f}"
        )
    
    def simulate_segregation(self,
                             type:str="default",
                             satisfaction:float=.5
                            ) -> str:
        map_copy = self.copy()
        
        for row in map_copy:
            for occupant in row:
                print(occupant.race)
        
        return 0
        
    

