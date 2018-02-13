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


# Class represent game croupier. It checks players card combinations and detects winner
class CroupierClass:
    def __init__(self, players_count, table, deck):
        self.players_count = players_count
        self.table = table
        self.players = []
        self.deck = deck
        # Store winner for each type of combination
        self.flush_winners = []
        self.straight_winners = []
        self.fours_winners = []
        self.full_house_winners = []
        self.sets_winners = []
        self.double_pairs_winners = []
        self.pairs_winners = []
        self.max_card_winners = []
        self.max_card_draw = False

    # Add players to table
    def add_player(self, player):
        if len(self.players) < self.players_count:
            self.players.append(player)
        else:
            raise ValueError("Too much players for this table!")

    # Distribute cards to players and table. After that - display cards in check combinations
    def start_game(self):
        for player in self.players:
            self.distribute_cards(player)
        self.distribute_cards(self.table)
        self.display_game()
        self.combinations_check()

    # Put cards in players hand
    def distribute_cards(self, player):
        while True:
            try:
                player.get_card(self.deck.drop_card())
            except ValueError:
                break

    # Show players card
    def display_game(self):
        for player in self.players:
            player.show_hand()
        self.table.show_hand()

    # Make one hand of players and table cards and order it
    def get_ordered_hand(self, player):
        ordered_hand = []
        for card in player.current_hand:
            ordered_hand.append(card.card_ranking)
        for table_card in self.table.current_hand:
            ordered_hand.append(table_card.card_ranking)
        return(sorted(ordered_hand, reverse=True))

    # Check possible poker combinations
    def combinations_check(self):
        suits_dict = {}
        # Count same suits at table. 3 suits of one type makes Flush possible
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
        self.check_fours()
        self.check_max_card()
        # Make final descision
        self.get_winner()

    # Check flush combination
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
        if len(winners_list) > 0:
            winners_list = sorted(winners_list, key=lambda tup: tup[1], reverse=True)
            self.flush_winners = winners_list[0]
            return True
        else:
            return False

    # Check straight combination
    def check_straight(self):
        winners_list = []
        for player in self.players:
            player_hand = self.get_ordered_hand(player)
            fails_counter = 0
            # Iterate over ordered hand in check, if player has each of consecutive 4 cards
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
        if len(winners_list) > 0:
            winners_list = sorted(winners_list, key=lambda tup: tup[1], reverse=True)
            self.straight_winners = winners_list[0]
            return True
        else:
            return False

    # Check fours, sets and pairs combinations
    def check_fours(self):
        pairs_list = []
        sets_list = []
        fours_list = []
        for player in self.players:
            local_pairs_list = []
            local_sets_list = []
            player_hand = self.get_ordered_hand(player)
            # Counts repeats of same card in each ordered hand
            for element1 in player_hand:
                repeat_counter = 0
                for element2 in player_hand:
                    if element1 == element2:
                        repeat_counter += 1
                if repeat_counter == 2:
                    local_pairs_list.append((player.name, element1))
                if repeat_counter == 3:
                    local_sets_list.append((player.name, element1))
                if repeat_counter == 4:
                    fours_list.append((player.name, element1))
            # Remove cases, when 6 pairs are counted
            if len(local_pairs_list) > 4:
                local_pairs_list = sorted(local_pairs_list, key=lambda tup: tup[1], reverse=True)
                local_pairs_list = local_pairs_list[:4]
            # Add player pairs to global pairs list
            pairs_list += local_pairs_list
            if len(local_sets_list) > 1:
                local_sets_list = sorted(local_sets_list, key=lambda tup: tup[1], reverse=True)
                sets_list.append(local_sets_list[0])
        if len(fours_list) > 0:
            fours_list = sorted(fours_list, key=lambda tup: tup[1], reverse=True)
            self.fours_winners = fours_list[0]
            return True
        sets_list = sorted(sets_list, key=lambda tup: tup[1], reverse=True)
        pairs_list = sorted(pairs_list, key=lambda tup: tup[1], reverse=True)
        # If sets and pairs were found - full house is possible
        if len(sets_list) > 0 and len(pairs_list) > 0:
            self.check_full_house(sets_list, pairs_list)
            self.sets_winners = sets_list[0]
            self.check_pairs(pairs_list)
        elif len(sets_list) > 0:
            self.sets_winners = sets_list[0]
        elif len(pairs_list) > 0:
            self.check_pairs(pairs_list)

    # Check full house combination (set + pair)
    def check_full_house(self, sets_list, pairs_list):
        if len(sets_list) == 1:
            possible_winner = sets_list[0][0]
            for element in pairs_list:
                if element[0] == possible_winner:
                    self.full_house_winners = element
                    return True
            return False
        else:
            for card_set in sets_list:
                possible_winner = sets_list[0][0]
                for element in pairs_list:
                    if element[0] == possible_winner:
                        self.full_house_winners = element
                        return True
            return False

    # Check pairs
    def check_pairs(self, pairs_list):
        if len(pairs_list) == 2:
            self.pairs_winners = pairs_list[0]
            return True
        for pair in pairs_list:
            possible_winner = pair[0]
            winner_pairs_counter = 0
            for other_pairs in pairs_list:
                if possible_winner == other_pairs[0]:
                    winner_pairs_counter += 1
            if winner_pairs_counter == 4:
                self.double_pairs_winners = pair
                return True
        self.pairs_winners = pairs_list[0]
        return True

    # Find max card in all players hands
    def check_max_card(self):
        current_max_card = 0
        current_winner = ""
        possible_draw_card = 0
        for player in self.players:
            ordered_hand = sorted(player.current_hand, key=lambda card: card.card_ranking, reverse=True)
            if ordered_hand[0].card_ranking > current_max_card:
                current_max_card = ordered_hand[0].card_ranking
                current_winner = player.name
            elif ordered_hand[0].card_ranking == current_max_card:
                possible_draw_card = current_max_card
        if possible_draw_card == current_max_card:
            self.max_card_draw = True
        else:
            self.max_card_winners = (current_winner, current_max_card)

    # Making final descision on winner
    def get_winner(self):
        if len(self.straight_winners) > 0 and len(self.flush_winners) > 0:
            if self.straight_winners == self.flush_winners:
                if self.straight_winners[1] == 12:
                    print("{} wins with ROYAL FLUSH!".format(self.straight_winners[0]))
                else:
                    print("{} wins with Straight Flush!".format(self.straight_winners[0]))
            elif len(self.fours_winners) > 0:
                print("{} wins with Fours!".format(self.fours_winners[0]))
            elif len(self.full_house_winners) > 0:
                print("{} wins with Full House!".format(self.full_house_winners[0]))
            else:
                print("{} wins with Flush!".format(self.flush_winners[0]))
        elif len(self.fours_winners) > 0:
            print("{} wins with Four of a kind!".format(self.fours_winners[0]))
        elif len(self.full_house_winners) > 0:
            print("{} wins with Full House!".format(self.full_house_winners[0]))
        elif len(self.flush_winners) > 0:
            print("{} wins with Flush!".format(self.flush_winners[0]))
        elif len(self.straight_winners) > 0:
            print("{} wins with Straight!".format(self.straight_winners[0]))
        elif len(self.sets_winners) > 0:
            print("{} wins with Three of a kind!".format(self.sets_winners[0]))
        elif len(self.double_pairs_winners) > 0:
            print("{} wins with Two pairs!".format(self.double_pairs_winners[0]))
        elif len(self.pairs_winners) > 0:
            print("{} wins with One pair!".format(self.pairs_winners[0]))
        elif self.max_card_draw:
            print("Draw!")
        else:
            print("{} wins with High card!".format(self.max_card_winners[0]))
            

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
