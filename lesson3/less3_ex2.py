import re

# Quizz word
prize_word = "python"
# Hide word with "_" symbols
hidden_word = "_" * len(prize_word)
# List of already inputed by player letters
used_letters = []


# Formatting string for better displaying, ex.: "p y t h o n"
def displaying_string(original_string):
    result_string = ""
    for letter in original_string:
        # Add whitespace after each string char
        result_string = result_string + letter + " "
    # Remove last whitespace and return formatted string
    return result_string.strip()


# Replacing char at defined position in string
def string_char_replace(original_string, index, replacement_char):
    result_string = ""
    original_string_len = len(original_string)
    iterator = 0
    # Iterate over original string and form new string
    while iterator < original_string_len:
        if iterator != index:
            result_string += original_string[iterator]
        else:
            # Add replacement char to result string instead of original at required index
            result_string += replacement_char
        iterator += 1
    return result_string


# Start game with displaying specialy formatted hidden word, ex.: "_ _ _ _ _ _"
print("Начинаем играть: " + displaying_string(hidden_word))
# Iterate while all "_" symbols will be replaced with proper letters
while "_" in hidden_word:
    user_input = input("Введите букву: ")
    # Check if user inputed more then one letter and return to the beginning in case of it
    if len(user_input) > 1:
        print("Пожалуйста, вводите не больше одной буквы!")
        continue
    # Check if player already inputed this letter
    elif user_input in used_letters:
        print("Такую букву уже называли!")
        continue
    # Find all positions of inputed letter in quizz word 
    found_letter_positions = list(re.finditer(user_input, prize_word))
    # Empty list means that letter was not found in quizz word
    if len(found_letter_positions) == 0:
        print("Нет такой буквы!")
        continue
    else:
        # Replace all "_" symbols at hidden word proper positions with correct letter
        for position in found_letter_positions:
            # Get char index from result of re.finditer
            char_index = position.start()
            # Replace "_" symbol
            hidden_word = string_char_replace(hidden_word, char_index, prize_word[char_index])
            # Add inputed letter to the list of used letters 
            used_letters.append(user_input)
        print("Есть такая буква: " + displaying_string(hidden_word))
# Finish quizz and display prize word
print("Поздравляем! Вы отгадали слово: " + displaying_string(hidden_word))