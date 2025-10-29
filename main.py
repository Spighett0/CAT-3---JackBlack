from random import *

def describeProject():
    print('\nAbout us: \n'
        'Our team consists of 3 members: Aaron, Ehen and Priya \n \n'
        'This project is a card game simulator It include options to shuffle a deck,' 
        'deal cards, show the top card and reset the deck. Users selct options by '
        'selcting a number, this program continues until the user chooses to quit. \n'
        'Our goals: \n' 
        '- To obtain 100% in this learning task \n'
        '- To beat Akira Yin Sau \n')
    # Add function stubs for all planned features. 
    # Implement one working function: describeProject() 
    # (8–12 lines describing goals, next steps, challenges, and learning). 
    # This should include  your about page from Task 1. 

def changelog():
    print('\nChangelog: \n'
    '(12/09/2025): \n' 
    '- Implemented new functions for cards in menu \n' 
    '- Added custom print messages for functions'
    '- Started on Task 3 and Task 4 \n \n' 
    '(10/10/2025): \n'
    '- This week we completed all of task 4 anf 5, making the Deck and Card classes \n'
    '- Began working on implementing code with the main menu \n' 
    '- Started blackjack \n'
    '(17/10/2025): \n'
    '- This week we finished implementing all of the codes from all of the seperate python files into main.py \n'
    '- Continued functionality with blackjack \n'
    '- Seperated the About us page and the changelog, and updated menu \n'
    '- Added if self._cards: loop for each of the card functions to bugfix error when there were no cards left')


Hand = []

class Card:
    def __init__(self, number, suit):
        self._suit=suit
        self.number= number
    def __repr__(self):
        return f"{self.number} of {self._suit}"
# Card class. takes in number and suit and then displays first number then suit
class deck: 
    def __init__(self):
        self._cards = []
        self.populate() 
    def populate(self):
        suits = ["hearts", "clubs", "diamonds", "spades"]
        numbers = [str(n) for n in range(2,11)] + ["Jack", "Queen", "King", "Ace"] # Creates number as a string between 2 to 11 and adds speical values
        self._cards = [ Card(n, s) for s in suits for n in numbers ]
        shuffle(self._cards)

    def showTopCard(self):
        if self._cards:
            return f'The top card in your deck is the {self._cards[0]}' # returns the top card in the list of self._cards
    
    def dealOne(self):
        if self._cards:
            Hand.append(self._cards[0]) # you append the first card of the deck to your hand
            del self._cards[0]
            return f"You have been dealt the {Hand[-1]}, and your hand now contains the {', '.join(map(str, Hand))}"
    
    def dealNth(self):
        if self._cards:
            n = int(input('Which card would you like to select? (number between 1 and 52) ')) # get an input from the user to pick a card
            if n > 0 and n < 53:
                n -= 1
                Hand.append(self._cards[n]) # append the chosen number
                del self._cards[n]
                return f"The card in spot {n+1} is {Hand[-1]}, and your hand currently contains the {', '.join(map(str, Hand))}"
            else:
                return 'Invalid card.'
    
    def funFact(self):
        if self._cards:
            cards = self._cards[:5] # creates a list as the first 5 cards in the deck
            cardlist = []

            for card in cards:
                cardlist.append(card.number) # appends the number of the card, card.number

            value_map = {
                "Ace": 14,
                "King": 13,
                "Queen": 12,
                "Jack": 11
            } # maps the face cards with numerical values to compare and find the maximum later on

            values = [value_map[n] if n in value_map else int(n) for n in cardlist] 
            # create a list called values to convert card.number into integers

            maximum = max(values) # takes the maximum of the values list using max()

            self.max_list = [cards[i] for i, v in enumerate(values) if v == maximum] 
            # creates max_list to have a list of the maximum valued cards in the top 5
            # this is to not have the code fail if there are multiple of the same max values

            self.max_ranks = ', '.join(map(str, self.max_list))
            first_five = ', '.join(map(str, self._cards[:5]))
            if len(self.max_list) == 1:
                return f"First five cards: {first_five}\nFun Fact:\nYour highest ranking card is {self.max_ranks}"
            else:
                return f"First five cards: {first_five}\nFun Fact:\nYour highest ranking cards are {self.max_ranks}"
        
    def viewDeck(self):
        return f"Your deck contains the {', '.join(map(str,self._cards))}"
    def __repr__(self):
        return f"First three cards are {', '.join(map(str,self._cards[:3]))}"

Deck = deck()
Deck.populate()

print()


def shuffleDeck():
    print('The deck has been shuffled')
    Deck.populate()

def dealOne():
    print('Dealing the top card')
    print(Deck.dealOne())

def dealNth():
    print('Dealing Nth card from the deck')
    print(Deck.dealNth())

def showTopCard():
    print('Showing top card from the deck')
    print(Deck.showTopCard())

def resetDeck():
    print('Resetting the deck to the original order')
    Deck.populate()

def funFact():
    print(Deck.funFact())

def viewDeck():
    print(Deck.viewDeck())



stop = False
while not stop:
    print(' \n1. About/Team \n'
    '2: View Changelog \n'
    '3: Shuffle the Deck \n'
    '4: Deal Top Card from the deck \n'
    '5: Deal Nth Card from the deck\n'
    '6: Show the Top Card\n'
    '7: Reset Deck \n'
    '8: Fun Fact from top 5 Cards \n'
    '9: View Deck \n'
    '10: Close Program \n')

    num = ''
    while num == "" or num.isnumeric() == False:
        num = input('What do you want to do? ')

    num = int(num)

    if num == 1:
        describeProject()
    elif num == 2:
        changelog()
    elif num == 3:
        shuffleDeck()
    elif num == 4:
        dealOne()
    elif num == 5:
        dealNth()
    elif num == 6:
        showTopCard()
    elif num == 7:
        resetDeck()
    elif num == 8:
        funFact()
    elif num == 9:
        viewDeck()
    elif num == 10:
        stop = True
    else:
        print('')

