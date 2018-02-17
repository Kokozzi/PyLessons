class Field:
    start_field = []
    ships = []
    enumerateted_letters = list(enumerate("АБВГДЕЖЗИК"))

    def __init__(self):
        self.start_field = [None for i in range(100)]
        required_ships = [(1, 4), (2, 3), (3, 2), (4, 1)]
        result = list(map(self.ship_generate, required_ships))

    def ship_generate(self, ship_params):
        for count in range(ship_params[0]):
            ship = Ship(ship_params[1])
            self.ask_ship_position(ship)
            self.ships.append(ship)

    def ask_ship_position(self, ship):
        possible_coords = []
        field_updated = True
        while True:
            if field_updated:
                self.display_game_field(self.start_field)
                field_updated = False
            user_input = input("Введите координаты {}-палубного корабля:".format(ship.length))
            converted_input = self.user_input_converter(user_input)

            if converted_input is None:
                continue
            if not self.free_coords_check(converted_input):
                print("Эти координаты уже заняты")
                continue
            if len(possible_coords) > 0 and converted_input not in possible_coords:
                print("Невозможно использовать эти координаты")
                continue

            ship.set_coord(converted_input)
            self.start_field[converted_input] = ship
            possible_coords = ship.get_next_possible_coords()
            field_updated = True
            # print(possible_coords)

            if ship.current_length == ship.length:
                break

        empty_cells = ship.get_empty_cells_coords()
        print(empty_cells)
        for cell in empty_cells:
            if self.free_coords_check(cell):
                self.start_field[cell] = EmptyCell(cell)

    def user_input_converter(self, user_input):
        try:
            letter = user_input[0].upper()
            number = int(user_input[1:]) - 1
        except ValueError:
            print("Координаты введены некорректно")
            return None

        letter_find = list(filter(lambda x: x[1] == letter, self.enumerateted_letters))
        if len(letter_find) == 0:
            print("Координаты введены некорректно")
            return None

        return letter_find[0][0] + number * 10

    def free_coords_check(self, coord):
        if self.start_field[coord] is not None:
            return False
        else:
            return True

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
            for letter_index in range(10):
                cell = game_field[(number - 1) * 10 + letter_index]
                if cell is None:
                    row += "   |"
                elif isinstance(cell, Ship):
                    row += " + |"
                elif isinstance(cell, EmptyCell):
                    row += " · |"
                else:
                    row += " x |"
            result += row + "\n" + separator
        print(result)


class Ship:
    length = 0
    current_length = 0
    coords = []

    def __init__(self, length):
        self.length = length
    
    def set_coord(self, coord):
        self.coords.append(coord)
        self.coords = sorted(self.coords)
        self.current_length += 1
        return self.current_length
    
    def hit(self, coord):
        self.current_length -= 1
        self.coords = list(filter(lambda x: x != coord, self.coords))
        return self.current_length

    def get_next_possible_coords(self):
        move_vertical = False
        move_horizontal = False
        if self.current_length < 2:
            move_vertical = True
            move_horizontal = True
        elif abs(self.coords[0] - self.coords[1]) == 1:
            move_horizontal = True
        else:
            move_vertical = True
        
        possible_coords = []
        if move_vertical:
            possible_coords += self.get_vertical_coords()
        if move_horizontal:
            possible_coords += self.get_horizontal_coords()
        return possible_coords
            
    def get_vertical_coords(self):
        if self.current_length == 0:
            raise ValueError("Wrong behaviour")

        start_coord = self.coords[0]
        finish_coord = self.coords[-1]
        possible_coords = []

        if start_coord < 10:
            possible_coords.append(finish_coord + 10)
        elif finish_coord >= 90:
            possible_coords.append(start_coord - 10)
        else:
            possible_coords.append(start_coord - 10)
            possible_coords.append(finish_coord + 10)
        
        return possible_coords
    
    def get_horizontal_coords(self):
        if self.current_length == 0:
            raise ValueError("Wrong behaviour")

        start_coord = self.coords[0] % 10
        finish_coord = self.coords[-1] % 10
        possible_coords = []

        if start_coord == 0:
            possible_coords.append(self.coords[-1] + 1)
        elif finish_coord == 9:
            possible_coords.append(self.coords[0] - 1)
        else:
            possible_coords.append(self.coords[0] - 1)
            possible_coords.append(self.coords[-1] + 1)
        
        return possible_coords

    def get_empty_cells_coords(self):
        empty_coords = []
        for used_cell in self.coords:
            print(used_cell)
            if used_cell % 10 == 0:
                empty_coords.append(used_cell + 1)
                if used_cell >= 10 and used_cell <= 89:
                    empty_coords.append(used_cell - 10)
                    empty_coords.append(used_cell - 9)
                    empty_coords.append(used_cell + 10)
                    empty_coords.append(used_cell + 11)
                elif used_cell < 10:
                    empty_coords.append(used_cell + 10)
                elif used_cell > 89:
                    empty_coords.append(used_cell - 10)
                continue
            if used_cell % 10 == 9:
                empty_coords.append(used_cell - 1)
                if used_cell >= 10 and used_cell <= 89:
                    empty_coords.append(used_cell - 10)
                    empty_coords.append(used_cell - 9)
                    empty_coords.append(used_cell + 10)
                    empty_coords.append(used_cell + 11)
                elif used_cell == 9:
                    empty_coords.append(used_cell + 10)
                elif used_cell > 89:
                    empty_coords.append(used_cell - 10)
                continue
            if used_cell % 10 != 0:
                empty_coords.append(used_cell - 1)
                if used_cell > 9:
                    if used_cell % 10 != 9:
                        empty_coords.append(used_cell - 9)
                    empty_coords.append(used_cell - 10)
                if used_cell >= 11:
                    empty_coords.append(used_cell - 11)
            if used_cell % 10 != 9:
                empty_coords.append(used_cell + 1)
                if used_cell < 90:
                    if used_cell % 10 != 0:
                        empty_coords.append(used_cell + 9)
                    empty_coords.append(used_cell + 10)
                if used_cell <= 88:
                    empty_coords.append(used_cell + 11)
        return list(set(empty_coords))


class EmptyCell:
    def __init__(self, coords):
        self.coord = coords


test = Field()