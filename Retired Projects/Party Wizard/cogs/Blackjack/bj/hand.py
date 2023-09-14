class Hand:
    def __init__(self):
        self._cards = []

    def getCards(self):
        return self._cards

    def addCard(self, card):
        self._cards.append(card)