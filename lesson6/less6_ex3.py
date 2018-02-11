from random import sample


# Generate random starting gamefield
def gamefield_generate():
    # Generate list with 0-15 numbers in random order
    numbers_order = sample(range(16), k=16)
    game_field = []
    row = 0
    number_iterator = 0
    # Forming 4x4 game field as list of 4 lists with 4 elements
    while row < 4:
        row_members = 0
        row_list = []
        # Forming each row by consequentially getting elements from random list 
        while row_members < 4:
            number_iterator += 1
            current_number = numbers_order[number_iterator - 1]
            if current_number == 0:
                # Store coordinates of empty field in separate tuple for easy access
                zero_coordinates = (row, row_members)
            row_list.append(current_number)
            row_members += 1
        game_field.append(row_list)
        row += 1
    return game_field, zero_coordinates


'''Format gamefield list for pretty displaying, ex:
____________________

| 6  | 10 | 4  | 1  |
____________________

| 9  | 12 | 13 | 5  |
____________________

| 7  | 15 | 14 | 8  |
____________________

| 2  | 3  |    | 11 |
____________________

'''
def display_gamefield(game_field):
    result_string = ""
    separator = "____________________\n\n"
    for row in game_field:
        result_string += separator
        displaying_row = ""
        # Forming row with whitespaces and "|" separators
        for number in row:
            displaying_row += "| "
            if number == 0:
                displaying_row += "   "
            elif number < 10:
                displaying_row += str(number) + "  "
            else:
                displaying_row += str(number) + " "
        displaying_row += "|\n"
        result_string += displaying_row
    result_string += separator
    return result_string


# Switch empty gamefiled space (presented as 0 in list) with number in other cell
def number_movement(game_field, zero_coordinates, move):
    error_move = False
    new_place = zero_coordinates
    # Detect movement direction based on user input
    if move == "left":
        # Check 0 coordinates to prevent moves outside the borders of gamefield
        if zero_coordinates[1] == 0:
            # Set Error flag in case of wrong move
            error_move = True
        else:
            # Calculate coordinates of switching cell 
            new_place = (zero_coordinates[0], zero_coordinates[1] - 1)
    elif move == "right":
        if zero_coordinates[1] == 3:
            error_move = True
        else:
            new_place = (zero_coordinates[0], zero_coordinates[1] + 1)
    elif move == "up":
        if zero_coordinates[0] == 0:
            error_move = True
        else:
            new_place = (zero_coordinates[0] - 1, zero_coordinates[1])
    elif move == "down":
        if zero_coordinates[0] == 3:
            error_move = True
        else:
            new_place = (zero_coordinates[0] + 1, zero_coordinates[1])
    if not error_move:
        # In case of allowed move switch two elements in list: 0 at zero_coordinates and number at new_place
        game_field[zero_coordinates[0]][zero_coordinates[1]], game_field[new_place[0]][new_place[1]] = game_field[new_place[0]][new_place[1]], game_field[zero_coordinates[0]][zero_coordinates[1]]
    return game_field, new_place, error_move


# Check current gamefield for possibility of solving
def solving_checker(game_field):
    formatted_field = []
    row_counter = 1
    zero_row_number = 0
    # Format gamefield from list of 4 lists into one list with 16 elements ("0" is replaced with "16")
    for row in game_field:
        for number in row:
            if number == 0:
                formatted_field.append(16)
                # Store numer of row where empty cell appeared
                zero_row_number = row_counter
            else:
                formatted_field.append(number)
        row_counter += 1
    
    pairs_counter = 0
    number_index = 0
    """
    Iterate over every element in formatted list except empty field (represented by "16")
    Consecutive compare every element with all next elements and count pairs, in which "next" element is greater than "current"
    After that add number of row with empty cell from `zero_row_number`
    """
    for number in formatted_field:
        # Pass calculations for empty cell
        if number == 16:
            continue
        # Stop calculations at last element
        if number_index == 15:
            break
        for next_number in formatted_field[number_index + 1:]:
            if next_number < number:
                pairs_counter += 1
        number_index += 1
    # Add number of row with empty cell to result
    pairs_counter += zero_row_number
    # Check if counter if ODD or EVEN
    if pairs_counter % 2 == 0:
        # EVEN counters means that quizz can be solved
        return True
    else:
        # ODD counters means that quizz can not be solved
        return False


# Winning combination of gamefield
win_result = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
# Store random gamefield and coordinates of 0 element (that presents empty space in gamefield)
game_field, zero_coordinates = gamefield_generate()
# Display gamefield for player
print(display_gamefield(game_field))

if solving_checker(game_field):
    print("Головоломка решаема!")
else:
    print("Головоломка нерешаема!")

# Run loop until current gamefield differs from winning combination
while game_field != win_result:
    move = input("Введите направление движения (left/right/up/down):").lower()
    # Check for correct player commands
    if move not in ["left", "right", "up", "down"]:
        print("Ошибка! Направление введено неправильно")
        continue
    # Switch empty field with number at inputed direction
    game_field, zero_coordinates, error_move = number_movement(game_field, zero_coordinates, move)
    if error_move:
        # Display result of impossible movements (trying to witch cells outside gamefield borders)
        print("Ход невозможен!")
    else:
        print(display_gamefield(game_field))

print("Поздравляю! Вы победили!")