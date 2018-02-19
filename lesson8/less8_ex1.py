import os

# Player's game field. Contains two lists - coordinated for placed ships and guesses.
class Field:
    # Enumerated list of letters for coordinates decode
    enumerateted_letters = list(enumerate("АБВГДЕЖЗИК"))
    # Total number of player's ships
    ships_count = 0

    def __init__(self, name):
        # Store player's name
        self.name = name
        # List with `Ship` objects
        self.ships = []
        # List for placed ships. At start fulled with `None`
        self.start_field = []
        self.start_field = [None for i in range(100)]
        # List of user's guesses
        self.guess_field = self.start_field.copy()
        # Ships that should be created in the beginning. Stores in tuples (`number of ships for this lenght`, `ships length`)
        required_ships = [(1, 4), (2, 3), (3, 2), (4, 1)]
        # Create required ships
        result = list(map(self.ship_generate, required_ships))
        # Display starting game field 
        self.display_game_field(self.start_field)
        # Finish prepearing part, move turn to another player
        input("Все корабли успешно размещены! Нажмите любую клавишу для передачи хода другому игроку.")
        # Clear console
        os.system('cls')

    # Create ships of reqiured length 
    def ship_generate(self, ship_params):
        # Loop counter depends on defined ships number of this length
        for count in range(ship_params[0]):
            # Create new Ship-type object
            ship = Ship(ship_params[1])
            # Ask user to input coordinates for this ship
            self.ask_ship_position(ship)
            # Add created ship to list and increase ships counter
            self.ships.append(ship)
            self.ships_count += 1

    # Ask user to input ship coordinates at game field
    def ask_ship_position(self, ship):
        # List of coordinates, that can be used during next choise
        possible_coords = []
        field_updated = True
        while True:
            # Flag, showing that game field was updated with new coordinates and displaying is required
            if field_updated:
                os.system('cls')
                self.display_game_field()
                field_updated = False
            # Ask user to input coordinates, ex: `А1`
            user_input = input("{}, введите координаты {}-палубного корабля:".format(self.name, ship.length))
            # Convert coordinates from Letter+Number to number only (list index)
            converted_input = self.user_input_converter(user_input)
            if converted_input is None:
                # Error during the convertation, ask again
                continue
            if not self.free_coords_check(converted_input):
                # Error during checking coordinates being already used
                print("Эти координаты уже заняты")
                continue
            if len(possible_coords) > 0 and converted_input not in possible_coords:
                # Inputed coords can not be allowed, for example they are too far from previous coords of this ship
                print("Невозможно использовать эти координаты")
                continue
            # Append coordinates to Ship object
            ship.set_coord(converted_input)
            # Mark that ship belongs to game field list with `converted_input` index
            self.start_field[converted_input] = ship
            # Calculate list of next possible coords
            possible_coords = ship.get_next_possible_coords()
            # Field was updated, set flag to True
            field_updated = True
            # Ship length reached requiered value, break loop
            if ship.current_length == ship.length:
                break
        # Get coordinates for required empty cells near new ship
        empty_cells = ship.get_empty_cells_coords()
        for cell in empty_cells:
            if self.free_coords_check(cell):
                # Set all free cells at requiered coordinates as EmptyCell objects
                self.start_field[cell] = EmptyCell(cell)

    # Convert inputed coordinates from Letter+Number format to number (gamefield's list index)
    def user_input_converter(self, user_input):
        try:
            # Try to split input into letter and number
            letter = user_input[0].upper()
            number = int(user_input[1:]) - 1
        except ValueError:
            print("Координаты введены некорректно")
            return None
        except IndexError:
            return None
        # Find letter in enumereated list to get it's index
        letter_find = list(filter(lambda x: x[1] == letter, self.enumerateted_letters))
        if len(letter_find) == 0:
            # Wrong letter was detected
            print("Координаты введены некорректно")
            return None
        # Generate index from letter index (column number) and number (row number)
        result = letter_find[0][0] + number * 10
        if result > 99:
            return None
        else:
            return result
    
    # Check is list's element at required index is None, that means empty cell 
    def free_coords_check(self, coord):
        if self.start_field[coord] is not None:
            return False
        else:
            return True

    # Display game_field list
    def display_game_field(self, game_field=None):
        if game_field is None:
            # Display start field as default value
            game_field = self.start_field
        # Field headers
        header = "    А   Б   В   Г   Д   Е   Ж   З   И   К\n"
        separator = "   ________________________________________\n"
        result = header + separator
        for number in range(1,11):
            # Generate each row
            num = str(number)
            if number < 10:
                row = num + " |"
            else:
                row = num + "|"
            for letter_index in range(10):
                # Generate each cell
                cell = game_field[(number - 1) * 10 + letter_index]
                if cell is None:
                    row += "   |"
                elif isinstance(cell, Ship):
                    row += " # |"
                elif isinstance(cell, EmptyCell):
                    row += " · |"
                else:
                    row += " x |"
            # Make finall result
            result += row + "\n" + separator
        print(result)

    # Check if ship was hitted during other player's guess
    def check_hit(self, coords):
        # Convert and check inputed coords
        coords = self.user_input_converter(coords)
        if coords is None:
            return False
        # Check if list element belongs to Ship class
        if isinstance(self.start_field[coords], Ship):
            ship = self.start_field[coords]
            # Make hit to found ship and check if its current length is not 0
            if ship.hit(coords) == 0:
                # Current length of ship is 0, it was destroyed. Decrease ships counter
                self.ships_count -= 1
                print("Корабль убит!")
            # Mark cell as successfully hitted
            self.start_field[coords] = HittedCell(coords)
            return True
        else:
            # Cell does not contain ship
            return False

    # Add marks to guess field. Hitted Cell `x` in case of successfull hit, Empty Cell in case of missing
    def add_guess(self, coords, success):
        coords = self.user_input_converter(coords)
        if coords is None:
            return False
        if success:
            self.guess_field[coords] = HittedCell(coords)
        else:
            self.guess_field[coords] = EmptyCell(coords)
        return True


# Represent each separate ship at gamefield
class Ship:
    # Length - required length of ship. Current_length - it current value, can be decreased by hit
    length = 0
    current_length = 0

    def __init__(self, length):
        self.length = length
        # List stores coordinates of ship at gamefield
        self.coords = []
    
    def set_coord(self, coord):
        # Add coordinate to full list of coordinates and sort it
        self.coords.append(coord)
        self.coords = sorted(self.coords)
        self.current_length += 1
        return self.current_length
    
    # Ship was hitted by correct guess of opposite player
    def hit(self, coord):
        # Decrease current ship length and remove hitted coordinate from list
        self.current_length -= 1
        self.coords = list(filter(lambda x: x != coord, self.coords))
        # Return current length for detecting of destroyed ships (thats length became 0)
        return self.current_length

    # Generate list of coordinates, that can be used during next turn for placing this ship
    def get_next_possible_coords(self):
        move_vertical = False
        move_horizontal = False
        # Small ships (one-cell length) can be continued horizontally or vertically
        if self.current_length < 2:
            move_vertical = True
            move_horizontal = True
        # Start of ship was placed horizontally, continue moving in this direction
        elif abs(self.coords[0] - self.coords[1]) == 1:
            move_horizontal = True
        # Case for vertical ships
        else:
            move_vertical = True
        
        possible_coords = []
        # Calculate possible coordinates in proper directions
        if move_vertical:
            possible_coords += self.get_vertical_coords()
        if move_horizontal:
            possible_coords += self.get_horizontal_coords()
        # Return final list of possible coordinates
        return possible_coords

    # Generate list of coordinates, that can be used for setting ship in vertical direction
    def get_vertical_coords(self):
        if self.current_length == 0:
            raise ValueError("Wrong behaviour")
        # Get coordinates of first and last ship cells
        start_coord = self.coords[0]
        finish_coord = self.coords[-1]
        possible_coords = []
        # Calculate indexes of allowed cells. They should be next to already used in this ship cells
        if start_coord < 10:
            # Top row, can move down only
            possible_coords.append(finish_coord + 10)
        elif finish_coord >= 90:
            # Bottom row, can move up only
            possible_coords.append(start_coord - 10)
        else:
            # Can move up and down 
            possible_coords.append(start_coord - 10)
            possible_coords.append(finish_coord + 10)
        
        return possible_coords

    # Generate list of coordinates, that can be used for setting ship in horizontal direction
    def get_horizontal_coords(self):
        if self.current_length == 0:
            raise ValueError("Wrong behaviour")
        # Get coordinates of first and last ship cells and detect their column index
        start_coord = self.coords[0] % 10
        finish_coord = self.coords[-1] % 10
        possible_coords = []
        # Calculate indexes of allowed cells. They should be next to already used in this ship cells
        if start_coord == 0:
            # First column, move to the right
            possible_coords.append(self.coords[-1] + 1)
        elif finish_coord == 9:
            # Last column, move to the left
            possible_coords.append(self.coords[0] - 1)
        else:
            # Can move to the left and rigth
            possible_coords.append(self.coords[0] - 1)
            possible_coords.append(self.coords[-1] + 1)
        
        return possible_coords

    # Generate list of empty cells, that should be near already placed ship 
    def get_empty_cells_coords(self):
        empty_coords = []
        for used_cell in self.coords:
            # Cells in first column
            if used_cell % 10 == 0:
                empty_coords.append(used_cell + 1)
                if used_cell >= 10 and used_cell < 90:
                    empty_coords.append(used_cell - 10)
                    empty_coords.append(used_cell - 9)
                    empty_coords.append(used_cell + 10)
                    empty_coords.append(used_cell + 11)
                # Cells in first row
                elif used_cell == 0:
                    empty_coords.append(used_cell + 10)
                    empty_coords.append(used_cell + 11)
                # Cells in last row
                elif used_cell == 90:
                    empty_coords.append(used_cell - 10)
                    empty_coords.append(used_cell - 9)
            # Cells in last column
            elif used_cell % 10 == 9:
                empty_coords.append(used_cell - 1)
                if used_cell > 10 and used_cell <= 89:
                    empty_coords.append(used_cell - 10)
                    empty_coords.append(used_cell - 11)
                    empty_coords.append(used_cell + 10)
                    empty_coords.append(used_cell + 9)
                # Cell in firsh row
                elif used_cell == 9:
                    empty_coords.append(used_cell + 10)
                    empty_coords.append(used_cell + 9)
                # Cell in last row
                elif used_cell == 99:
                    empty_coords.append(used_cell - 10)
                    empty_coords.append(used_cell - 11)
            # All cells between first and last columns
            else:
                empty_coords.append(used_cell - 1)
                empty_coords.append(used_cell + 1)
                if used_cell > 9:
                    empty_coords.append(used_cell - 9)
                    empty_coords.append(used_cell - 10)
                if used_cell >= 11:
                    empty_coords.append(used_cell - 11)
                if used_cell <= 88:
                    empty_coords.append(used_cell + 11)
                if used_cell < 90:
                    empty_coords.append(used_cell + 9)
                    empty_coords.append(used_cell + 10)
        return list(set(empty_coords))


# Empty cell, that can not be used for placing ships
class EmptyCell:
    def __init__(self, coords):
        self.coord = coords


# Cell that was successfully hitted
class HittedCell:
    def __init__(self, coords):
        self.coord = coords


# Game master, that controlls players turns and detects winner
class GameMaster:
    def __init__(self):
        # List of players
        self.players = []
        # Indexes for player, that will guess, and for player that will check hits 
        self.guess_player_index = 0
        self.check_player_index = 1
    
    # Add player to current game session
    def add_player(self, player):
        self.players.append(player)

    # Start game loop
    def start_game(self):
        os.system("cls")
        while True:
            # Check if one of player lost all ships
            for player in self.players:
                if player.ships_count == 0:
                    print("{} проиграл!".format(player.name))
                    return
            # Start player's turn and repeat it in case of sucessful hit
            if not self.turn():
                # In case of miss move turn to another player
                self.move_turn()
                os.system("cls")
                input("Промах! Ход переходит к другому игроку. Нажмите любую клавишу.")
                print("\n\n")

    # Move turn between players
    def move_turn(self):
        self.guess_player_index, self.check_player_index = self.check_player_index, self.guess_player_index

    # Player's guess turn
    def turn(self):
        # Detect witch player will guess and witch will check
        guess_player = self.players[self.guess_player_index]
        check_player = self.players[self.check_player_index]
        # Display guessing field for player
        guess_player.display_game_field(guess_player.guess_field)
        # Ask for inputting coordinates
        guess = input("Ход игрока {}. Введите координаты выстрела: ".format(guess_player.name))
        # Check inputed coordinates for successful hit
        if check_player.check_hit(guess):
            # Ship was hitted, display it at guess game_field
            guess_player.add_guess(guess, True)
            os.system("cls")
            print("Попадание! Ход продолжается.\n")
            return True
        # Missing guess, display guess at game_field
        guess_player.add_guess(guess, False)
        return False

# Create gamemaster with two players and start game
gamemaster = GameMaster()
gamemaster.add_player(Field("Alice"))
gamemaster.add_player(Field("Bob"))
gamemaster.start_game()