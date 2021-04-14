from .hand import Hand
class Player:

 
    def __init__(self, name):
        self._name = name
        self._balance = 0
        self._hand = Hand()
        self._halue = 0    
    def pay(self, amount):
        self._balance = self._balance - amount
    
    def win(self, amount):
        self._balance = self._balance + amount
    
    def getBalance(self):
        return self._balance

    def addCard(self, card):
        # print(f"(debug) {self._name} pulled a(n) " + card)
        self._hand.addCard(card)
        self.evaluate()

    def resetHand(self):
        self._hand = Hand()

    def getNumCards(self):
        return len(self.getCards())
    
    def getDecision(self):
        _decision = input("Pull another card, or stop?\n")
        if _decision == 'pull':
            return True
        elif _decision == 'stop':
            return False
        else:
            print("Not a valid input, sorry!")
    
    def setValue(self, value):
        self._halue = value

    def printCards(self):
        print(f"{self._name}'s Cards are: {self._hand.getCards()}")
    
    def getValue(self):
        return self._halue

    def evaluate(self):
        values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'J':10, 'Q':10, 'K':10, 'A':11}
        _value = 0
        aces = 0
        for card in self._hand.getCards():
            if values[card[:1]] == 11:
                aces += 1
            else:
                _value += values[card[:1]]
        
        while aces > 0:
            if _value + aces * 11 <= 21:
                _value += 11
                aces -= 1
            else:
                _value += 1
                aces -= 1
        self.setValue(_value)
        # print(f"{self._name}'s hand is now valued at {str(_value)}.")
        return _value

    def over(self):
        return self.getValue() > 21
