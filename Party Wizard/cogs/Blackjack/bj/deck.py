_ctypes = ['2', '3', '4', '5', '6', '7', '8', '9', 'Jack', 'Queen', 'King', 'Ace']
_cSuits = [' of Hearts', ' of Clubs', ' of Diamonds', ' of Spades']
import random as rd
class Deck:

    _cards = []

    def __init__(self, size):
        for _ in range(size):
            for i in range(len(_ctypes)):
                for j in range(len(_cSuits)):
                    self._cards.append(_ctypes[i] + _cSuits[j])

    def pickCard(self):
        temp = rd.randint(0, len(self._cards) - 1)
        return self._cards.pop(temp)
    
    def getCards(self):
        return self._cards
    
    def printCards(self):
        print(_cards)



