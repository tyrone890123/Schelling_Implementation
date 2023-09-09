import random
from utils.custom_exceptions import (NotInRegionError)
from utils.utils import (txt_to_grid)
from utils.Occupant import Occupant
        
class GridMap:
    def __init__(self, 
                 grid: list):
        self.grid = txt_to_grid(grid)
        self.shape = self._get_shape() # (x-size, y-size)
        self.population = self._count_race()
        self.total = (self.shape[0]*self.shape[1])
        
    def _get_shape(self, 
                   grid: list[list[Occupant]] = None
                   ) -> (int, int):
        """
        
        Function to get the shape of the matrix NxN 
        
        """
        if grid is None:
            grid = self.grid
        return (len(grid[0]),len(grid))
    
    def _grid_to_sep_str(self, 
                         grid: list[list[Occupant]] = None) -> list[str]:
        """
        
        Function to get new line separated grid
        
        """
        if grid is None:
            grid = self.grid
            
        combined_str = []
        for row in grid:
            sep_grid = [occupant.race for occupant in row]
            combined_str.append(" ".join(sep_grid))
        return combined_str
            
    def _grid_to_str(self, 
                     grid: list[list[Occupant]] = None
                     ) -> str:
        """
        
        Function for converting grid to string
        
        """
        if grid is None:
            grid = self.grid
            
        return "\n".join(self._grid_to_sep_str(grid))
    
    def _count_race(self, 
                    grid: list[list[Occupant]] = None) -> dict:
        """
        
        Fuction for getting population count
        
        """
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

    def _get_random_subregion(self, 
                              subregion_size: int
                              ) -> list[list[Occupant]]:
        """
        
        Function for getting a random subregion inside of the region
        
        """
        
        #get random starting point
        rand_x = (random.randint(0,self.shape[0]-subregion_size))
        rand_y = (random.randint(0,self.shape[1]-subregion_size))
        
        #limit y axis to the rand_y value
        sub_region = self.grid[rand_y:rand_y+subregion_size+1]
        for idx,row in enumerate(sub_region):
            # for each row limit x to rand_x value
            sub_region[idx] = row[rand_x:rand_x+subregion_size+1]
        return sub_region
    
    def _verify_subregion(self, 
                          sub_region: list[list[Occupant]]
                          ) -> bool:
        """
        
        Used to verify if inputted subregion is actually part of the region
        
        """
        
        # get subregion shape for creating the same NxN for checking
        sub_region_shape = (len(sub_region[0]), len(sub_region))
        stringed_sub_region = self._grid_to_str(sub_region)   
         
        correct = 0
        for y in range(0,self.shape[1]-sub_region_shape[1]+1):
            for x in range(0,self.shape[0]-sub_region_shape[0]+1):
                # loop through the same size and get a snapshot for checking
                # similarity between region and sub region inputted
                chunk = self.grid[y:y+sub_region_shape[1]]
                for idx,row in enumerate(chunk):
                    chunk[idx] = row[x:x+sub_region_shape[0]]
                if self._grid_to_str(chunk) == stringed_sub_region:
                    correct+=1
                    break
        return correct
    
    def _get_neighbors(self, 
                       coord: (int,int), 
                       grid: list[list[Occupant]] = None
                       ) -> list[Occupant]: 
        if grid is None:
            grid = self.grid
        
        # displace current point to top right
        """
        
        X 0 X
          V -- this is where the coord should be
        X X 0
        X 0 0
        
        V -- displace pointer to this point for easier looping
        X 0 X
        X X 0
        X 0 0
        
        """
        x = coord[0] - 1
        y = coord[1] - 1
        
        # get the max values for x and y to avoid
        grid_shape = self._get_shape(grid)
        max_x = grid_shape[0] - 1
        max_y = grid_shape[1] - 1
        
        neighbors = []
        for y_disp in range(0,3):
            for x_disp in range(0,3):
                new_x = x + x_disp
                new_y = y + y_disp
                
                # ignore current point
                if coord[0] != new_x or coord[1] != new_y:
                    
                    # Checks whether the point is at the edge
                    if (new_x >= 0 
                        and new_x <= max_x 
                        and new_y >= 0 
                        and new_y <= max_y):
                        # if not grid[new_y][new_x].is_empty():
                        neighbors.append(grid[new_y][new_x])
        return neighbors
    
    def _compute_satisfaction(self, 
                              curr_point: (int, int), 
                              neighbors: list[Occupant]
                              ) -> float:
        """
        
        Function for computing satisfaction of an occupant based on neighbors
        
        """
        sides = len(neighbors)
        similar = 0
        
        for neighbor in neighbors:
            if neighbor.race == curr_point.race:
                similar += 1
                
        return float(similar/sides)
    
    def _get_empty_spots(self, grid):
        vacant_list = []
        for row in grid:
            for occupant in row:
                if occupant.is_empty():
                    vacant_list.append(occupant)

        return vacant_list
    
    def copy(self, 
             grid: list[list[Occupant]] = None
             ) -> list[list[Occupant]]:
        """
        
        Function for copying the grid objects
        
        """
        if grid is None:
            grid = self.grid
            
        copy_grid = []
        for row in grid:
            holder = []
            for occupant in row:
                holder.append(occupant.copy())
            copy_grid.append(holder)
        return copy_grid
        
    def print_grid(self,
                   grid: list[list[Occupant]] = None
                   ) -> None:
        """
        
        Prints a grid object
        
        """
        if grid is None:
            grid = self.grid
            
        print(self._grid_to_str(grid))
    
    def get_dissimilarity_index(self, 
                                sub_region: str = None,
                                subregion_size: int = 4
                                ) -> None:
        
        """
        
        Used to solve for the dissimilarity index
        
        """
        if sub_region is None:
            sub_region = self._get_random_subregion(subregion_size)
        else:
            if not self._verify_subregion(sub_region):
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
    
    def simulate_segregation(self,
                             type:str="default",
                             satisfaction:float=.5,
                             target_iterations = 20
                            ) -> str:
        
        """
        
        Function for simulating the schelling segregation process
        
        """
        map_copy = self.copy()
        
        if type == "default":
            for y,row in enumerate(self.grid):
                for x,occupant in enumerate(row):
                    neighbors = self._get_neighbors((x,y), self.grid)
                    if (self._compute_satisfaction(occupant, neighbors) 
                        < satisfaction):
                        map_copy[y][x].delete()       
            self.print_grid(map_copy)
            
        if type == "relocate":
            num_iterations = 0
            while True:
                num_dissatisfied = 0
                for y,row in enumerate(map_copy):
                    for x,occupant in enumerate(row):
                        
                        #skip if location is empty
                        if not occupant.is_empty():
                            
                            # verify if current occupant is dissatisfied
                            neighbors = self._get_neighbors((x,y), map_copy)
                            if (self._compute_satisfaction(occupant, neighbors) 
                                < satisfaction):
                                
                                # get all possible spots to relocate
                                moving_locs = self._get_empty_spots(map_copy)
                                
                                # track best score for relocation
                                best_score = (0,None)
                                for loc in moving_locs:
                                    loc_x = loc.location[0]
                                    loc_y = loc.location[1]
                                    
                                    test_map = self.copy(map_copy)
                                    test_map[y][x].delete()
                                    test_map[loc_y][loc_x].set_race(occupant.race)
                                    curr = test_map[loc_y][loc_x]
                                    neighbors = self._get_neighbors(
                                        (loc_x,loc_y), 
                                        test_map
                                    )
                                    if (best_score[0] 
                                        < self._compute_satisfaction(curr, neighbors)):
                                        best_score = (
                                            self._compute_satisfaction(curr, neighbors), 
                                            loc.location
                                        )
                                
                                # once the best loc is available we relocate
                                best_loc = best_score[1]
                                map_copy[best_loc[1]][best_loc[0]].set_race(occupant.race)
                                map_copy[y][x].delete()
                
                # check number of dissatisfied in grid
                for y,row in enumerate(map_copy):
                    for x,occupant in enumerate(row):
                        neighbors = self._get_neighbors((x,y), map_copy)
                        if (self._compute_satisfaction(occupant, neighbors) 
                            < satisfaction):
                            num_dissatisfied+=1
                num_iterations+=1
                
                # checks if theres no more dissatisfied or target iterations 
                # reached
                if (not num_dissatisfied 
                    or num_iterations == target_iterations):
                    break
            
            satisfied_percent = float(
                (self.total - num_dissatisfied) 
                / self.total
            )
            
            print(f"Percent Satisfied: {satisfied_percent*100}")
            self.print_grid(map_copy)
        
        return 0
        
    

