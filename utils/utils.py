import logging

from utils.custom_exceptions import (NotEqualMatrixError)
from utils.Occupant import Occupant

logging.basicConfig(
    format='%(asctime)s - %(message)s', 
    level=logging.INFO
)

def read_input(path: str) -> list[str]:
    """
    
    Function for reading file input to str list
    
    """
    x_len = None
    raw_matrix = []
    with open(path) as f:
        for idx, line in enumerate(f.readlines()):
            # cant use strip() since it removes trailing white spaces
            curr_line = line.replace('\n','')
            
            # catches invalid matrix size
            if idx == 0:
                x_len = len(curr_line)
            if len(curr_line) != x_len:
                raise NotEqualMatrixError("Please Input an NxN matrix")
            else:
                raw_matrix.append(curr_line)
    return raw_matrix
    
def txt_to_grid(map: list[str]) -> list[list[Occupant]]:
    """
    
    Function for converting string list to 2d array of occupants
    
    """
    grid = []
    for y,row in enumerate(map):
        grid_row = []
        for x,occupant in enumerate(row):
            grid_row.append(Occupant(occupant,(x,y)))
        grid.append(grid_row)
    return grid