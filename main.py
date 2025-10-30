from random import shuffle

suits = ["hearts", "clubs", "diamonds", "spades"]
numbers = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]

# ---------- Card and Deck ----------
class Card:
    def __init__(self, number, suit):
        self._suit = suit
        self.number = number

    def value(self):
        if self.number in ["Jack", "Queen", "King"]:
            return 10
        elif self.number == "Ace":
            return 11 
        else:
            return int(self.number)

    def __repr__(self):
        return f"{self.number} of {self._suit}"

class Deck:
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.populate()

    def populate(self):
        self._cards = [Card(n, s) for _ in range(self.num_decks) for s in suits for n in numbers]
        shuffle(self._cards)

    def deal(self):
        if not self._cards:
            self.populate()
        return self._cards.pop()

# ---------- Hand ----------
class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def total(self):
        value = sum(c.value() for c in self.cards)
        aces = sum(1 for c in self.cards if c.number == "Ace")
        # Adjust for aces
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def __repr__(self):
        return ", ".join(str(c) for c in self.cards)

    def is_bust(self):
        return self.total() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.total() == 21

# ---------- Game Logic ----------
class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.balance = 1000

    def play_round(self):
        print(f"\nBalance: ${self.balance}")
        bet = input("Place your bet: $")
        if not bet.isdigit():
            print("Invalid bet.")
            return
        bet = int(bet)
        if bet <= 0 or bet > self.balance:
            print("Invalid bet amount.")
            return

        self.balance -= bet
        player = Hand()
        dealer = Hand()

        player.add(self.deck.deal())
        dealer.add(self.deck.deal())
        player.add(self.deck.deal())
        dealer.add(self.deck.deal())

        print(f"\nDealer shows: {dealer.cards[0]}")
        print(f"Your hand: {player} (value: {player.total()})")


        if player.is_blackjack():
            if dealer.is_blackjack():
                print("Both have blackjack! Push.")
                self.balance += bet
            else:
                print("Blackjack! You win 3:2 payout.")
                self.balance += int(bet * 2.5)
            return

        while True:
            print("\n1. Hit\n2. Stand\n3. Stop Program")
            choice = input("What do you want to do? ")

            if choice == "1":
                player.add(self.deck.deal())
                print(f"Your hand: {player} (value: {player.total()})")
                if player.is_bust():
                    print("You busted! Dealer wins.")
                    return
            elif choice == "2":
                break
            elif choice == "3":
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice. Try again.")

        print(f"\nDealer's hand: {dealer} (value: {dealer.total()})")
        while dealer.total() < 17:
            dealer.add(self.deck.deal())
            print(f"Dealer hits: {dealer} (value: {dealer.total()})")

        p_val, d_val = player.total(), dealer.total()
        if dealer.is_bust():
            print(f"Dealer busts! You win ${bet}.")
            self.balance += bet * 2
        elif p_val > d_val:
            print(f"You win! {p_val} vs Dealer {d_val}")
            self.balance += bet * 2
        elif p_val == d_val:
            print("Push. You keep your bet.")
            self.balance += bet
        else:
            print(f"Dealer wins {d_val} vs {p_val}.")

    def start(self):
        print("=== Blackjack Text Edition ===")
        while self.balance > 0:
            self.play_round()
            again = input("\nPlay again? (y/n): ").lower()
            if again != 'y':
                break
        print(f"\nGame over! Final balance: ${self.balance}")

if __name__ == "__main__":
    Blackjack().start()
