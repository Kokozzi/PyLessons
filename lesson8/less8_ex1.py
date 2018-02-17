class WarField:
    start_field = {}
    guess_field = {}
    ships = []
    possible_letters = "АБВГДЕЖЗИК"
    enumerateted_letters = list(enumerate(possible_letters))

    def __init__(self):
        for cell in [j + str(i) for j in self.possible_letters for i in range(1,11)]:
            self.start_field[cell] = None
        self.guess_field = self.start_field.copy()
        self.display_game_field(self.start_field)
        self.start_field_generate()

    def display_game_field(self, game_field):
        header = "    А   Б   В   Г   Д   Е   Ж   З   И   К\n"
        separator = "   ________________________________________\n"
        result = header + separator
        for number in range(1,11):
            num = str(number)
            if number < 10:
                row = num + " |"
            else:
                row = num + "|"
            for letter in self.possible_letters:
                if game_field[letter + num] is None:
                    row += "   |"
                elif game_field[letter + num] is True:
                    row += " + |"
                elif game_field[letter + num] is False:
                    row += " · |"
                else:
                    row += " x |"
            result += row + "\n" + separator
        print(result)

    def start_field_generate(self):
        required_ships = [(1, 4), (2, 3), (3, 2), (4, 1)]
        result = list(map(self.place_ship, required_ships))
    
    def place_ship(self, ship_definitions):
        for current_ship in range(ship_definitions[0]):
            ship = Ship(ship_definitions[1])
            self.ships.append(ship)
            possible_next_coords = []
            while True:
                user_coords = input("Введите координаты {}-палубного корабля:".format(ship_definitions[1]))
                user_coords = user_coords.upper()
                if user_coords not in self.start_field:
                    print("Введены неверные координаты!")
                    continue
                if len(possible_next_coords) > 0 and user_coords not in possible_next_coords:
                    print("Эти координаты не могут быть использованы!")
                    continue
                if self.start_field[user_coords] is not None:
                    print("Клетка уже занята!")
                    continue
                self.start_field[user_coords] = True
                self.display_game_field(self.start_field)
                ship.set_coord(user_coords)
                if ship.current_length != ship.length:
                    possible_next_coords = self.get_possible_coords(user_coords, ship.coords)
                else:
                    break
            # self.set_ships_separators(full_ship_coords)
            return True
    
    def get_possible_coords(self, current_coord, full_ship_coords):
        letter_index = [x[0] for x in self.enumerateted_letters if x[1] == current_coord[0]]
        if len(letter_index) == 0:
            raise ValueError("Impossible coordinates")
        else:
            letter_col = letter_index[0]

        move_horizontal, move_vertical = False, False

        if len(full_ship_coords) <= 1:
            move_horizontal, move_vertical = True, True
        if len(full_ship_coords) == len(list(filter(lambda x: x[0] == full_ship_coords[0][0],full_ship_coords))):
            move_vertical = True
        else:
            move_horizontal = True
        
        possible_letters_variants = []
        if move_horizontal:
            possible_letters_variants = self.get_horizontal_coords(letter_col, full_ship_coords)
        
        number_index = int(current_coord[1:])
        possible_number_variants = []
        if move_vertical:
            possible_number_variants = self.get_vertical_coords(number_index, full_ship_coords)

        vertical = [current_coord[0] + number for number in possible_number_variants]
        horizontal = [letter + current_coord[1:] for letter in possible_letters_variants]
        result = list(filter(lambda x: self.start_field[x] is None, vertical + horizontal))
        print(result)
        return result
    
    def get_vertical_coords(self, number_index, full_ship_coords):
        result = []

        if len(full_ship_coords) > 1:
            full_ship_coords = sorted(full_ship_coords, key=lambda x: int(x[1:]))
            start_point = int(full_ship_coords[0][1:])
            finish_point = int(full_ship_coords[-1][1:])
        else:
            start_point = number_index
            finish_point = number_index
        
        if start_point == 1:
            result.append(str(finish_point + 1))
        elif finish_point == 10:
            result.append(str(start_point - 1))
        else:
            result.append(str(finish_point + 1))
            result.append(str(start_point - 1))
        
        print("vertical", result)
        return result
    
    def get_horizontal_coords(self, letter_col, full_ship_coords):
        result = []

        if len(full_ship_coords) > 1:
            full_ship_coords = sorted(full_ship_coords, key=lambda x: x[0])
            start_letter = full_ship_coords[0][0]
            start_point = [x[0] for x in self.enumerateted_letters if x[1] == start_letter][0]
            finish_letter = full_ship_coords[-1][0]
            finish_point = [x[0] for x in self.enumerateted_letters if x[1] == finish_letter][0]
        else:
            start_point = letter_col
            finish_point = letter_col

        if start_point == 0:
            result.append(self.enumerateted_letters[finish_point + 1][1])
        elif finish_point == 9:
            result.append(self.enumerateted_letters[start_point - 1][1])
        else:
            result.append(self.enumerateted_letters[finish_point + 1][1])
            result.append(self.enumerateted_letters[start_point - 1][1])
        print("horizontal", result)
        return result

    # def set_ships_separators(self, full_ship_coords):
    #     if len(full_ship_coords) == 1:
    #         ship_coords = full_ship_coords[0]
    #         letter_index = [x[0] for x in self.enumerateted_letters if x[1] == ship_coords[0]][0]
    #     elif len(full_ship_coords) > 1:
    #         full_ship_coords = sorted(full_ship_coords, key=lambda x: x[0])
    #         start_letter = full_ship_coords[0][0]
    #         start_point = [x[0] for x in self.enumerateted_letters if x[1] == start_letter][0]
    #         finish_letter = full_ship_coords[-1][0]
    #         finish_point = [x[0] for x in self.enumerateted_letters if x[1] == finish_letter][0]
    #     else:
    #         raise ValueError("Wrong ship size detected")


class Ship:
    length = 0
    current_length = 0
    coords = []

    def __init__(self, length):
        self.length = length
    
    def set_coord(self, coord):
        self.coords.append(coord)
        self.current_length += 1
        return self.current_length
    
    def hit(self, coord):
        self.current_length -= 1
        self.coords = list(filter(lambda x: x != coord, self.coords))
        return self.current_length


player1 = WarField()
