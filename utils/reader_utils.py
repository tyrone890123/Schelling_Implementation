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
                 grid: list):
        self.grid = txt_to_grid(grid)
        self.shape = self._get_shape() # (x-size, y-size)
        self.population = self._count_race()
        
    def _get_shape(self, grid = None):
        if grid is None:
            grid = self.grid
        return (len(grid[0]),len(grid))
    
    def _grid_to_sep_str(self, grid = None):
        if grid is None:
            grid = self.grid
        combined_str = []
        for row in grid:
            combined_str.append(" ".join([occupant.race for occupant in row]))
        return combined_str
            
    def _grid_to_str(self, grid = None):
        if grid is None:
            grid = self.grid
        return "\n".join(self._grid_to_sep_str(grid))
    
    def _count_race(self, grid=None):
        if grid is None:
            grid = self.grid
        population = {}
        for row in grid:
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
        sub_region = self.grid[rand_y:rand_y+subregion_size+1]
        for idx,row in enumerate(sub_region):
            sub_region[idx] = row[rand_x:rand_x+subregion_size+1]
        return sub_region
    
    def copy(self):
        return self.grid.copy()
        
    def print_grid(self,grid=None):
        if grid is None:
            grid = self.grid
        print(self._grid_to_str(grid))
    
    def verify_subregion(self, sub_region):
        sub_region_shape = (len(sub_region[0]), len(sub_region))
        stringed_sub_region = self._grid_to_str(sub_region)    
        correct = 0
        for y in range(0,self.shape[1]-sub_region_shape[1]+1):
            for x in range(0,self.shape[0]-sub_region_shape[0]+1):
                chunk = self.grid[y:y+sub_region_shape[1]]
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
        dissimilarity_index = abs(val1-val2)/2
        
        print(
            f"DISSIMILARITY INDEX: {dissimilarity_index}"
            f" or {dissimilarity_index:.3f}"
        )
        
    def _get_neighbors(self, coord, grid = None):
        if grid is None:
            grid = self.grid
            
        x = coord[0]-1
        y = coord[1]-1
        
        grid_shape = self._get_shape(grid)
        max_x = grid_shape[0]-1
        max_y = grid_shape[1]-1
        
        neighbors = []
        for y_disp in range(0,3):
            for x_disp in range(0,3):
                new_x = x+x_disp
                new_y = y+y_disp
                # ignore self
                if coord[0] != new_x or coord[1] != new_y:
                    # checks for edges
                    if (new_x >= 0 
                        and new_x <= max_x 
                        and new_y >= 0 
                        and new_y <= max_y):
                        # if not grid[new_y][new_x].is_empty():
                        neighbors.append(grid[new_y][new_x])
        return neighbors
    
    def _compute_satisfaction(self, curr_point, neighbors):
        sides = len(neighbors)
        similar = 0
        
        for neighbor in neighbors:
            if neighbor.race == curr_point.race:
                similar += 1
                
        return float(similar/sides)
    
    def simulate_segregation(self,
                             type:str="default",
                             satisfaction:float=.5
                            ) -> str:
        map_copy = []
        
        if type == "default":
            for y,row in enumerate(self.grid):
                holder = []
                for x,occupant in enumerate(row):
                    neighbors = self._get_neighbors(occupant.location, self.grid)
                    if self._compute_satisfaction(occupant, neighbors)>=satisfaction:
                        holder.append(self.grid[y][x])
                    else:
                        holder.append(Occupant(" ",(x,y)))
                map_copy.append(holder)       
            self.print_grid(map_copy)
        
        return 0
        
    

