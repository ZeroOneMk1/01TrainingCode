from .consts import DISTANCES

class Road():
    def __init__(self, trip: str, type: str) -> None:
        self.type = type
        self.trip = trip
        self.length = self.evaluate()
    
    
    def evaluate(self) -> int:
        working = 0
        
        for i in range(0, len(self.trip) -1):
            working += DISTANCES[ord(self.trip[i]) - ord("A")][ord(self.trip[i+1]) - ord("A")]
        
        working += DISTANCES[0][ord(self.trip[0]) - ord("A")]
        working += DISTANCES[ord(self.trip[-1]) - ord("A")][0]
        
        return working
