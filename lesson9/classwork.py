import json

def read_file(filename):
    with open(filename) as f:
        return f.read()


def write_file(filename, text, mode="a"):
    with open(filename, mode=mode) as f:
        f.write(text)


# write_file("hello.txt", "\nQ2222111111111", mode="w")
# print(read_file("hello.txt"))


import requests

def get_site(url):
    site = requests.get(url)
    print(site.status_code)


# get_site("http://ya.ru")

import re

nasa_file = read_file("./lesson9/nasa_19950801.tsv.txt")
nasa_splitted = re.split(r'\n+', nasa_file)
date_dict = {}
url_dict = {}
response_dict = {}
index = 0
for line in nasa_splitted[1:]:
    splitted_string = re.split(r'\t+', line)

    if splitted_string[2] in date_dict:
        date_dict[splitted_string[2]] += 1
    else:
        date_dict[splitted_string[2]] = 1

    if splitted_string[4] in url_dict:
        url_dict[splitted_string[4]] += 1
    else:
        url_dict[splitted_string[4]] = 1
    
    if splitted_string[5] in response_dict:
        response_dict[splitted_string[5]] += 1
    else:
        response_dict[splitted_string[5]] = 1

date_dict = sorted(date_dict, key=date_dict.get, reverse=True)
print(date_dict)
print(url_dict)
url_dict = sorted(url_dict, key=url_dict.get, reverse=True)
print(url_dict)