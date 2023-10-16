class Pot:
    def __init__(self):
        self._value = 0
    
    def getValue(self):
        return self._value

    def addToPot(self, amount):
        self._value += amount
    
    def reset(self):
        self._value = 0

    def printValue(self):
        print(self._value)