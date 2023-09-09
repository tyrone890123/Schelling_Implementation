import argparse
from utils.reader_utils import (GridMap,read_input)

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--path", 
                      help="input path to data to be processed")
    args.add_argument("-sp", "--sr_path",
                      help="input path to subregion")
    return args.parse_args()

if __name__ == "__main__":
    args = get_args()
    file_read = read_input(args.path)
    subregion_read = read_input(args.sr_path)
    map = GridMap(file_read)
    
    map.get_dissimilarity_index(subregion=subregion_read)