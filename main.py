from random import *

suits = ["hearts", "clubs", "diamonds", "spades"]
numbers = [str(n) for n in range(2,11)] + ["Jack", "Queen", "King", "Ace"] 

class Card:
    def __init__(self, number, suit):
        self._suit = suit
        self.number = number

    def value(self):
        return self.number

    def __repr__(self):
        return f"{self.number} of {self._suit}"

class Deck: 
    def __init__(self, num_decks=4):
        self._cards = []
        self.num_decks = num_decks
        self.populate() 

    def populate(self):
        self._cards = [ Card(n, s) for s in suits for n in numbers ]
        shuffle(self._cards)

    def deal(self):
        if self._cards:
            return self._cards.pop()
        else:
            self.populate()
            return self._cards.pop()
    
class Hand:
    def __init__(self):
        self._cards = []

    def add(self, card):
        self._cards.append(card)

    def values(self):
        total = 0
        aces = 0
        for c in self._cards:
            total += c.value()
            if c.rank == 'A':
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        return len(self._cards) == 2 and self.values() == 21

    def is_bust(self):
        return self.values() > 21

    def can_split(self):
        return len(self._cards) == 2 and self._cards[0].value() == self._cards[1].value()

    def copy(self):
        h = Hand()
        h.cards = self._cards.copy()
        return 
    
    def __repr__(self):
        return self.cards

deck = Deck()
deck.populate()
deck.deal()
hand1 = Hand

print(hand1)

stop = False
while not stop:
    print('1. Hit \n'
    '2. Stand \n' 
    '3. Stop Program')

    num = ''
    while num == "" or num.isnumeric() == False:
        num = input('What do you want to do? ')

    num = int(num)

    if num == 1:
        break
    elif num == 2:
        break
    elif num == 3:
        stop = True
    else:
        print('')

