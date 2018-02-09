from random import shuffle

class DeckClass:
    def __init__(self):
        possible_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        possible_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.card_pack = []
        for card in possible_cards:
            for suit in possible_suits:
                self.card_pack.append(CardClass(card, suit))
    def shuffle(self):
        # self.card_pack = shuffle(self.card_pack)
        return self.card_pack


class CardClass:
    def __init__(self, card_number, suit):
        self.card_number = card_number
        self.suit = suit
    def __repr__(self):
        return str(self.card_number) + " of " + str(self.suit)


class PlayerClass:
    def __init__(self, hand_size):
        self.hand_size = hand_size


my_deck = DeckClass()
for card in my_deck.card_pack:
    print(card)
print("\n")
print(my_deck.shuffle())