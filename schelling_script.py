import argparse

from utils.utils import logging
from utils.custom_exceptions import InvalidPercentRange
from utils.GridMap import (GridMap)
from utils.utils import(read_input,
                        txt_to_grid)

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--path", 
                      help="input path to data to be processed")
    args.add_argument("-sp", "--sr_path",
                      help="input path to subregion")
    args.add_argument("-t", "--seg_type",
                      default="default",
                      help="input segregation method [default|relocate]")
    args.add_argument("--satisfaction",
                      default="0.5",
                      help="input satisfaction percent in decimal")
    args.add_argument("-n", "--num_iterations",
                      default="20",
                      help="input satisfaction percent in decimal")
    return args.parse_args()

if __name__ == "__main__":
    args = get_args()
    
    logging.info("READING FILE")
    file_read = read_input(args.path)
    grid = GridMap(file_read)
    
    logging.info("FILE OUTPUT")
    grid.print_grid()
    print("\n")
    
    SUB_REGION_PATH = args.sr_path
    SATISFACTION_SET = args.satisfaction
    ITERATIONS = args.num_iterations
    
    if SUB_REGION_PATH:
        subregion_read = txt_to_grid(read_input(SUB_REGION_PATH))
    
    if SATISFACTION_SET:
        try:
            satisfaction = float(SATISFACTION_SET)
            if satisfaction>1 or satisfaction<0:
                raise InvalidPercentRange("Invalid value inputted")
        except ValueError:
            raise "Invalid input type"
    
    if ITERATIONS:
        try:
            iterations = float(ITERATIONS)
            if satisfaction>1 or satisfaction<0:
                raise InvalidPercentRange("Invalid value inputted")
        except ValueError:
            raise "Invalid input type"
    
    logging.info("GETTING INDEX OF DISSIMILARITY")
    grid.get_dissimilarity_index(subregion_read)
    print("\n")
    
    logging.info("SIMULATING SCHELLING SIMULATION")
    grid.simulate_segregation(type = args.seg_type,
                              satisfaction = satisfaction,
                              target_iterations = iterations)