class Occupant:
    def __init__(self, 
                 race: str, 
                 location: tuple):
        self.race = race
        self.location = location
        
    def delete(self) -> None:
        """
        
        Function for vacating the current occupant
        
        """
        self.race = " "
    
    def is_empty(self) -> None:
        """
        
        Function for checking if current occupant is empty
        
        """
        return self.race == " "
    
    def set_race(self, incoming:str) -> None:
        """
        
        Function for setting the race of the occupant
        
        """
        self.race = incoming
    
    def copy(self):
        """
        
        Function for creating a copy of the current object
        
        """
        return Occupant(self.race, self.location)