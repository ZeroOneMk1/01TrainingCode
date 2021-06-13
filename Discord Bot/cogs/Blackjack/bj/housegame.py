from .player import Player
from .pot import Pot
from .deck import Deck
import json

class Game:
    def __init__(self, size = 1):
        self._p1 = Player("Player 1")
        self._house = Player("House")
        self._pot = Pot()
        self._deck = Deck(size)
        self._running = True
        self._p1playing = True
        self.inround = True

    def jsonify(self):
        return json.dumps(self.__dict__)

    def play(self):

        while self._running:

            self._pot.addToPot(int(input("How much do you bet on this round?\n")))
            self.inround = True
            self._p1playing = True

            self._p1.addCard(self._deck.pickCard())
            self._p1.addCard(self._deck.pickCard())
            self._house.addCard(self._deck.pickCard())

            self._p1.printCards()
            self._house.printCards()

            self._house.addCard(self._deck.pickCard())


            while self.inround:
                if self._p1playing:
                    if self._p1.getDecision():
                        self._p1.addCard(self._deck.pickCard())
                        self._p1.printCards()
                        if self._p1.over():
                            self._p1playing = False
                    else:
                        self._p1playing = False
                        self._house.printCards()

                elif self._p1.over():
                    self._p1.pay(self._pot.getValue())
                    self._pot.reset()
                    self.inround = False
                    self._house.printCards()
                    
                elif not self._p1playing and not self._p1.over():

                    if not self._house.getValue() > self._p1.getValue():
                        self._house.addCard(self._deck.pickCard())
                        self._house.printCards()
                        

                        if self._house.over():
                            self._p1.win(self._pot.getValue())
                            self._pot.reset()
                            self.inround = False
                    else:
                        self._p1.pay(self._pot.getValue())
                        self._pot.reset()
                        self.inround = False

            print('Round over\n')
            self._p1.resetHand()
            self._house.resetHand()
            print("Your balance is " + str(self._p1.getBalance()))

            if not int(input("Do you want to keep playing? 1  for yes, 0 for no.\n")):
                self._running = False