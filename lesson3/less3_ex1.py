import re

# Forming lists with languages alphabets (based on letters codes) 
en_alphabet = list(map(chr, range(ord("a"), ord("z") + 1)))
ru_alphabet = list(map(chr, range(ord("а"), ord("я") + 1)))

# test strings
test_string_en = "The quick brown fox jumps over the lazy dog"
# missing letters - "w" and "n"
wrong_string_en = "The quick bro fox jumps over the lazy dog"
test_string_ru = "Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства."


# Check string language 
def language_check(checking_string):
    string_language = None
    iterator = 0
    # Consistently looking for user's string symbols in prepared alphabets. First coincidence finishes loop.
    while string_language == None:
        if checking_string[iterator] in en_alphabet:
            string_language = "en"
        elif checking_string[iterator] in ru_alphabet:
            string_language = "ru"
        else:
            iterator += 1
    # Return language code ("en"/"ru") or None in case of unknown langage
    return string_language


# Check string for containing all alphabet letters
def alphabet_check(checking_string, alphabet):
    # List of missed in user's string letters 
    missing_letters = []
    # Iterate over alphabet and look for coincidences in user's string. 
    for letter in alphabet:
        if letter not in checking_string:
            # In case of missing letter in string - append it to missing letters list
            missing_letters.append(letter)
    # Return list of missing alphabet letters. Will be empty for Pangrams 
    return missing_letters


# Check if string is english or russian Pangram
def pangram_check(examinated_string):
    # Remove all not-alphabet symbols from examinated string and make it lower case
    examinated_string = re.sub("\W+", "", examinated_string.lower())
    # Try to detect string language
    string_language = language_check(examinated_string)
    # Check for containing all language's alphabet letters in string
    if string_language == "en":
        missing_letters = alphabet_check(examinated_string, en_alphabet)
    elif string_language == "ru":
        missing_letters = alphabet_check(examinated_string, ru_alphabet)
    else:
        # Raise error in case of unknown language
        raise ValueError("Wrong language detected!")
    # Empty missing_letters list means that string is Pangram
    if len(missing_letters) == 0:
        return "String is Pangram!"
    else:
        # Print string, containing all missing letters from language alphabet
        return "String is not Pangram, missing letters: " + ", ".join(missing_letters)

try:
    print(pangram_check(test_string_ru))
except ValueError as error_text:
    print(error_text)

try:
    print(pangram_check(test_string_en))
except ValueError as error_text:
    print(error_text)

try:
    print(pangram_check(wrong_string_en))
except ValueError as error_text:
    print(error_text)