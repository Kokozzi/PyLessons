from random import shuffle

# Class representing card deck. Contains list of card objects.
class DeckClass:
    def __init__(self):
        # Possible values of card numbers and card suits
        possible_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        possible_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        # List of cards in deck
        self.card_pack = []
        # Generate all possible combinations of numbers and suits
        for card in possible_cards:
            for suit in possible_suits:
                # Append card object to deck
                self.card_pack.append(CardClass(card, suit))
        # Randomly shuffle the list of cards
        self.shuffle()
    # Shuffles list of cards randomly
    def shuffle(self):
        shuffle(self.card_pack)
        return self.card_pack
    # Picks card from list 
    def drop_card(self):
        return self.card_pack.pop()


# Class representing card. Contains number and suit attributes
class CardClass:
    def __init__(self, card_number, suit):
        self.card_number = card_number
        self.suit = suit
    # Form proper representaion, ex.: "8 of Clubs"
    def __repr__(self):
        return str(self.card_number) + " of " + str(self.suit)


# Class representing player. Contains list of current player's cards and max hand size
class PlayerClass:
    def __init__(self, hand_size):
        # Max number of cards that player can get
        self.hand_size = hand_size
        # List of all cards in player's hand
        self.current_hand = []
    # Appends card to list in hand limit is not reached
    def get_card(self, card):
        if len(self.current_hand) < self.hand_size:
            self.current_hand.append(card)
        else:
            raise ValueError("Hand is full")
    # Display list of cards in player's hand
    def show_hand(self):
        print(self.current_hand)


# Form card's deck
my_deck = DeckClass()
# Form player with hand size limit of 5 cards
player1 = PlayerClass(5)
# Loop until player hand will not reach limit
while True:
    try:
        # Put card in player's hand from deck
        player1.get_card(my_deck.drop_card())
    except ValueError:
        # Hand limit was reached, exit from loop
        break
# Display cards in player's hand
player1.show_hand()
