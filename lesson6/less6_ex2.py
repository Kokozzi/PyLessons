from random import shuffle

# Class representing card deck. Contains list of card objects.
class DeckClass:
    def __init__(self):
        # Possible values of card numbers and card suits
        possible_cards = enumerate([2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"])
        # print(list(possible_cards))
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
        self.card_displaying = card_number[1]
        self.card_ranking = card_number[0]
        self.suit = suit

    # Form proper representaion, ex.: "8 of Clubs"
    def __repr__(self):
        return str(self.card_displaying) + " of " + str(self.suit)


# Class representing player. Contains list of current player's cards and max hand size
class PlayerClass:
    def __init__(self, hand_size, name):
        # Max number of cards that player can get
        self.hand_size = hand_size
        # List of all cards in player's hand
        self.current_hand = []
        # Player's displaying name
        self.name = name

    # Appends card to list in hand limit is not reached
    def get_card(self, card):
        if len(self.current_hand) < self.hand_size:
            self.current_hand.append(card)
        else:
            raise ValueError("Hand is full")

    # Display list of cards in player's hand
    def show_hand(self):
        print("{}: {}".format(self.name, self.current_hand))


class CroupierClass:
    def __init__(self, players_count, table, deck):
        self.players_count = players_count
        self.table = table
        self.players = []
        self.deck = deck
        self.flush_winners = []
        self.straight_winners = []
        self.fours_winners = []

    def add_player(self, player):
        if len(self.players) < self.players_count:
            self.players.append(player)
        else:
            raise ValueError("Too much players for this table!")

    def start_game(self):
        for player in self.players:
            self.distribute_cards(player)
        self.distribute_cards(self.table)
        self.display_game()
        self.combinations_check()

    def distribute_cards(self, player):
        while True:
            try:
                player.get_card(self.deck.drop_card())
            except ValueError:
                break

    def display_game(self):
        for player in self.players:
            player.show_hand()
        self.table.show_hand()

    def combinations_check(self):
        suits_dict = {}
        for card in self.table.current_hand:
            if card.suit in suits_dict:
                suits_dict[card.suit]["count"] += 1
                suits_dict[card.suit]["max_card"] = max(suits_dict[card.suit]["max_card"], card.card_ranking)
            else:
                suits_dict[card.suit] = {"count": 1, "max_card": card.card_ranking}
        for suit, counter in suits_dict.items():
            if counter["count"] >= 3:
                self.check_flush(suit, counter)
                break
        self.check_straight()
        self.get_winner()

    def check_flush(self, suit, count):
        players_result = {}
        winners_list = []
        for player in self.players:
            players_result[player.name] = count.copy()
            for card in player.current_hand:
                if card.suit == suit:
                    players_result[player.name]["count"] += 1
                    players_result[player.name]["max_card"] = max(players_result[player.name]["max_card"], card.card_ranking)
            if players_result[player.name]["count"] == 5:
                winners_list.append((player.name, players_result[player.name]["max_card"]))
        winners_list = sorted(winners_list, key=lambda tup: tup[1], reverse=True)
        self.flush_winners = winners_list[0]

    def get_ordered_hand(self, player):
        ordered_hand = []
        for card in player.current_hand:
            ordered_hand.append(card.card_ranking)
        for table_card in self.table.current_hand:
            ordered_hand.append(table_card.card_ranking)
        return(sorted(ordered_hand, reverse=True))

    def check_straight(self):
        winners_list = []
        for player in self.players:
            player_hand = self.get_ordered_hand(player)
            fails_counter = 0
            for element in player_hand:
                n = 1
                if fails_counter < 3:
                    while True:
                        if element - n not in player_hand:
                            fails_counter += 1
                            break
                        elif n == 4:
                            winners_list.append((player.name, element))
                            break
                        else:
                            n += 1
                else:
                    break
        winners_list = sorted(winners_list, key=lambda tup: tup[1], reverse=True)
        self.straight_winners = winners_list[0]
    
    def check_fours(self):
        pairs_list = []
        sets_list = []
        fours_list = []
        for player in self.players:
            player_hand = self.get_ordered_hand(player)
            for element1 in player_hand:
                repeat_counter = 0
                for element2 in player_hand:
                    if element1 == element2:
                        repeat_counter += 1
                if repeat_counter == 2:
                    pairs_list.append((player.name, element1))
                if repeat_counter == 3:
                    sets_list.append((player.name, element1))
                if repeat_counter == 4:
                    fours_list.append((player.name, element1))
            if len(pairs_list > 2):
                pairs_list = sorted(pairs_list, key=lambda tup: tup[1], reverse=True)
                pairs_list = pairs_list[:2]
        fours_list = sorted(fours_list, key=lambda tup: tup[1], reverse=True)
        self.fours_winners = fours_list[0]

    def get_winner(self):
        if len(self.straight_winners) > 0 and len(self.flush_winners) > 0:
            if self.straight_winners == self.flush_winners:
                if self.straight_winners[1] == 12:
                    print("{} wins with ROYAL FLUSH!".format(self.straight_winners[0]))
                else:
                    print("{} wins with Straight Flush!".format(self.straight_winners[0]))
            elif len(self.fours_winners) > 0:
                    print("{} wins with Fours!".format(self.fours_winners[0]))
            else:
                print("{} wins with Flush!".format(self.flush_winners[0]))
        elif len(self.straight_winners) > 0:
            print("{} wins with Straight!".format(self.straight_winners[0]))
        elif len(self.flush_winners) > 0:
            print("{} wins with Flush!".format(self.flush_winners[0]))
        else:
            print("Winner unknown")
            


# Form card's deck
my_deck = DeckClass()
# Form two players with hand size limit of 2 cards
player1 = PlayerClass(2, "Alice")
player2 = PlayerClass(2, "Bob")
# Form table with hand size limit of 5 cards
table = PlayerClass(5, "Table")

croupier = CroupierClass(2, table, my_deck)
croupier.add_player(player1)
croupier.add_player(player2)
croupier.start_game()
