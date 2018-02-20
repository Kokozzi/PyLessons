import re

# Open file for reading
def read_file(filename):
    with open(filename) as f:
        return f.read()

# Display keys with max values from dict, limited by values_number
def display_top_values(user_dict, name ,values_number):
    # Sort dict by values and get first `values_number` elements
    top_values_list = sorted(user_dict, key=user_dict.get, reverse=True)[:values_number]
    iterator = 1
    print("Top-{} {} matches:".format(values_number, name))
    # Print each value in pretty form
    for value in top_values_list:
        print("{}: {} - {} matches".format(iterator, value, user_dict[value]))
        iterator += 1
    print()

# Open file for reading
nasa_file = read_file("./lesson9/nasa_19950801.tsv.txt")
# Split file's text into lines 
nasa_splitted = re.split(r'\n+', nasa_file)
# Dicts for storing required parsed data
date_dict = {}
url_dict = {}
response_dict = {}

# Iterate over lines (without first line with headers)
for line in nasa_splitted[1:]:
    # Split line by tabs
    splitted_string = re.split(r'\t+', line)
    # Avoid empty strings
    if len(splitted_string) < 6:
        continue
    # Forming dict for date/time values
    if splitted_string[2] in date_dict:
        date_dict[splitted_string[2]] += 1
    else:
        date_dict[splitted_string[2]] = 1
    # Forming dict for urls values
    if splitted_string[4] in url_dict:
        url_dict[splitted_string[4]] += 1
    else:
        url_dict[splitted_string[4]] = 1
    # Formint dict for response codes
    if splitted_string[5] in response_dict:
        response_dict[splitted_string[5]] += 1
    else:
        response_dict[splitted_string[5]] = 1

# Display tol-10 values from each dict
display_top_values(date_dict, "Time", 10)
display_top_values(url_dict, "URL", 10)
display_top_values(response_dict, "Response code", 10)
