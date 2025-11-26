import tkinter as tk 
from PIL import Image, ImageTk
import os 
from main import *
from random import shuffle # Using the shuffle import from your new logic


root = tk.Tk()
CARD_WIDTH, CARD_HEIGHT = 100, 145
START_X = 20
Y_PLAYER = 250
Y_DEALER = 50
X_OFFSET = 120 
BG_COLOR = '#004225'
CARD_DIR = "D:\\School\\GITHUB\\CAT-3---JackBlack\\Cardspng" 

root.title("JackBlack - Simple GUI")
root.config(bg=BG_COLOR)
root.geometry('850x550')
root.resizable(False, False)

# Initialize Game State
game = Blackjack()
photo_references = [] # Holds Tkinter PhotoImage objects (to prevent garbage collection)
current_labels = []   # Holds Tkinter Label widgets for cards


status_label = tk.Label(root, text="Press Deal to start!", font=('Arial', 24, 'bold'), fg='gold', bg=BG_COLOR)
status_label.place(x=300, y=10)

balance_label = tk.Label(root, text=f"Balance: ${game.balance}", font=('Arial', 14), fg='white', bg=BG_COLOR)
balance_label.place(x=150, y=10)

dealer_score_label = tk.Label(root, text="Dealer: ?", font=('Arial', 16), fg='white', bg=BG_COLOR)
dealer_score_label.place(x=10, y=10)

player_score_label = tk.Label(root, text="Player: 0", font=('Arial', 16), fg='white', bg=BG_COLOR)
player_score_label.place(x=10, y=220)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.place(x=20, y=470)

hit_btn = tk.Button(button_frame, text="HIT", state=tk.DISABLED, font=('Arial', 14), bg='red', fg='white', width=10)
hit_btn.pack(side=tk.LEFT, padx=10)

stand_btn = tk.Button(button_frame, text="STAND", state=tk.DISABLED, font=('Arial', 14), bg='blue', fg='white', width=10)
stand_btn.pack(side=tk.LEFT, padx=10)

deal_btn = tk.Button(button_frame, text="DEAL", font=('Arial', 14), bg='green', fg='white', width=10)
deal_btn.pack(side=tk.LEFT, padx=10)


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def get_card_filename(card: Card, face_up=True):
    """Converts a Card object or uses a card back for the filename."""
    if face_up:
        # Uses the Card.__repr__ format (e.g., 'A of Spades')
        # We no longer replace spaces with underscores, as the user indicated spaces are used.
        filename = str(card) 
        full_path = os.path.join(CARD_DIR, f"{filename}.png")
    else:
        # Assumes 'Card_Back_Red.png' is the card back image in the same directory
        full_path = os.path.join(CARD_DIR, "Card_Back_Red.png") 
    
    return full_path

def clear_cards():
    """Removes all card labels from the screen."""
    for label in current_labels:
        label.destroy()
    current_labels.clear()
    photo_references.clear()
    
def draw_cards(cards: list[Card], start_y, hide_first=False):
    """Draws a list of cards starting at a given position."""
    
    for i, card in enumerate(cards):
        face_up = True
        if hide_first and i == 0:
            face_up = False
            
        file_path = get_card_filename(card, face_up)
        
        try:
            # Requires PIL/Pillow for image handling
            card_image = Image.open(file_path)
            resized_image = card_image.resize((CARD_WIDTH, CARD_HEIGHT))
            tk_image = ImageTk.PhotoImage(resized_image)
            
            photo_references.append(tk_image)
            
            label = tk.Label(root, image=tk_image, borderwidth=0, highlightthickness=0)
            label.place(x=START_X + (i * X_OFFSET), y=start_y)
            current_labels.append(label)

        except FileNotFoundError:
            # Fallback for missing images
            placeholder_text = "BACK" if not face_up else f"{get_card_gui_rank(card.number)}\n{card._suit.capitalize()}"
            placeholder = tk.Label(root, 
                                   text=placeholder_text, 
                                   width=14, height=7, bg='gray', fg='white',
                                   font=('Arial', 12, 'bold'))
            placeholder.place(x=START_X + (i * X_OFFSET), y=start_y)
            current_labels.append(placeholder)
        except Exception as e:
            # This handles potential issues with PIL/Tkinter integration
            print(f"An unexpected error occurred: {e}")
            
# =========================================================
# 5. CORE GAME LOGIC FUNCTIONS (Using the integrated Blackjack class)
# =========================================================

def update_ui(player_turn=True, final_reveal=False):
    """Redraws the cards and updates the score labels."""
    clear_cards()

    player_hand = game.player_hand
    dealer_hand = game.dealer_hand

    # 1. Draw Player Cards
    draw_cards(player_hand.cards, Y_PLAYER)
    player_score_label.config(text=f"Player: {player_hand.total()}")

    # 2. Draw Dealer Cards
    draw_cards(dealer_hand.cards, Y_DEALER, hide_first=not final_reveal)
    
    if final_reveal:
        dealer_score_label.config(text=f"Dealer: {dealer_hand.total()}")
    else:
        # Only show the value of the visible card (second card)
        visible_value = dealer_hand.cards[1].value() if len(dealer_hand.cards) > 1 else 0
        dealer_score_label.config(text=f"Dealer: {visible_value}")

    # Update button states
    # If game.running is False, buttons are disabled (except DEAL)
    if player_turn and game.running:
        hit_btn.config(state=tk.NORMAL)
        stand_btn.config(state=tk.NORMAL)
        deal_btn.config(state=tk.DISABLED)
    else:
        hit_btn.config(state=tk.DISABLED)
        stand_btn.config(state=tk.DISABLED)
        deal_btn.config(state=tk.NORMAL)
        
    balance_label.config(text=f"Balance: ${game.balance}")
    root.update() # Force UI refresh


def check_end_condition():
    """Compares hands and determines the winner."""
    # game.running is already set to False by the caller (hit or stand)
    p_val = game.player_hand.total()
    d_val = game.dealer_hand.total()
    bet = 100 # Fixed bet for simplicity

    # Ensure final card view is shown
    update_ui(player_turn=False, final_reveal=True)

    result_text = ""
    bet_amount = 0

    if p_val > 21:
        result_text = f"BUST! You lose ${bet}."
        bet_amount = -bet
    elif d_val > 21:
        result_text = f"Dealer busts! You win ${bet}."
        bet_amount = bet
    elif game.player_hand.is_blackjack() and len(game.player_hand.cards) == 2:
        result_text = "BLACKJACK! You win 3:2!"
        bet_amount = int(bet * 1.5)
    elif p_val > d_val:
        result_text = f"You win! {p_val} vs Dealer {d_val}."
        bet_amount = bet
    elif p_val == d_val:
        result_text = "PUSH. Bet returned."
        bet_amount = 0
    else:
        result_text = f"Dealer wins {d_val} vs {p_val}."
        bet_amount = -bet

    game.balance += bet_amount
    status_label.config(text=result_text, fg='cyan')
    # MODIFIED: Explicitly set final_reveal=True here so the dealer's hand remains visible
    # after the final status message, until the DEAL button is pressed.
    update_ui(player_turn=False, final_reveal=True) 


def dealer_play():
    """The dealer reveals their face-down card and hits until 17 or more."""
    status_label.config(text="Dealer's Turn...", fg='yellow')
    
    # Reveal the hidden card
    update_ui(player_turn=False, final_reveal=True)
    root.update()
    
    # Dealer hits below 17
    def dealer_hit_sequence():
        # Check if game is still running (important if user closes window prematurely)
        if not root.winfo_exists():
            return
        
        if game.dealer_hand.total() < 17 and not game.dealer_hand.is_bust():
            game.dealer_hand.add(game.deck.deal())
            update_ui(player_turn=False, final_reveal=True)
            root.after(500, dealer_hit_sequence) # Schedule next hit with a delay
        else:
            check_end_condition() # Game ends after dealer stops hitting

    # Use 'root.after' for delay instead of time.sleep
    root.after(500, dealer_hit_sequence)


def hit():
    """Handles the Player's 'Hit' action."""
    # Check 1: If game.running is False (set by a previous bust or stand), exit immediately.
    if not game.running: return
    
    game.player_hand.add(game.deck.deal())
    update_ui(player_turn=True)
    
    if game.player_hand.is_bust():
        # FIX FOR SPAM BUG:
        # 1. Immediately set game.running to False. This makes the check at the start of 'hit()' block subsequent clicks.
        game.running = False 
        
        # 2. Immediately update the UI to disable HIT/STAND buttons.
        # This uses the 'else' block inside update_ui() since game.running is now False.
        update_ui(player_turn=False) 

        # 3. Schedule the final scoring check.
        root.after(500, check_end_condition)


def stand():
    """Handles the Player's 'Stand' action and starts the Dealer's turn."""
    if not game.running: return
    game.running = False # Set running to false immediately when standing
    dealer_play()


def deal_new_game():
    """Starts a new round of blackjack."""
    bet = 100 # Fixed bet for simplicity

    if game.balance < bet:
        status_label.config(text="Game Over! Out of funds.", fg='red')
        deal_btn.config(state=tk.DISABLED)
        return
        
    game.deck.populate()
    game.player_hand = Hand()
    game.dealer_hand = Hand()
    game.running = True

    # Deal initial cards
    game.player_hand.add(game.deck.deal())
    game.dealer_hand.add(game.deck.deal())
    game.player_hand.add(game.deck.deal())
    game.dealer_hand.add(game.deck.deal())

    status_label.config(text="Your Turn: Hit or Stand?", fg='white')
    
    update_ui(player_turn=True)
    
    # Check for initial Blackjack
    if game.player_hand.is_blackjack():
        # Immediately set running to false before scheduling the end condition
        game.running = False
        # Delay to show initial cards before ending
        root.after(500, check_end_condition) 


# =========================================================
# 6. BIND FUNCTIONS TO BUTTONS AND START APPLICATION
# =========================================================

hit_btn.config(command=hit)
stand_btn.config(command=stand)
deal_btn.config(command=deal_new_game)

# Start the game loop
deal_new_game()

root.mainloop()