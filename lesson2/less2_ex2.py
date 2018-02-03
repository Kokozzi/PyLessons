import re

example_text = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"

example_text.lower()

# Dict will contain every unique word from text as a key and number of matches for this word as a value
words_counters = dict()

# Replace all not-word characters (punctuations, whitespaces) with one witespace character
example_text = re.sub("\W+", " ", example_text)
# Remove witespaces from the beginning and end of string. After that - split string by whitespaces and store it as list
splitted_text = example_text.strip().split(" ")

for word in splitted_text:
    if word != "":
        # Filling Dict with unique words from text. In case of repeating word several times - increase counter storing in val()
        if word in words_counters:
            words_counters[word] += 1
        else:
            words_counters[word] = 1

# Get items from Dict (presented by tuples (word, frequency_counter)) and sort them by decreasing counter number
sorted_words = sorted(words_counters.items(), key=lambda word_tuple: word_tuple[1], reverse=True)

# Displaying top-10 words by its frequency
place_index = 0
while place_index < 10:
    # Formatting example: "4. text_word - 2 times"
    print("{}. {} - {} times".format(str(place_index + 1), sorted_words[place_index][0], sorted_words[place_index][1]))
    place_index += 1
