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
    
    def set_race(self, incoming):
        self.race = incoming
    
    def copy(self):
        return Occupant(self.race, self.location)