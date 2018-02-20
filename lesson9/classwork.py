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
