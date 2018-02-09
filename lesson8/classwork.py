# Generator
# print((element for element in "12345678"))

def fib():
    a,b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen_fib = fib()
# print(next(gen_fib))
# print(next(gen_fib))
# print(next(gen_fib))

import random

def random_generator(from_int, to_int):
    while True:
        yield random.randint(from_int, to_int)

rand_gen = random_generator(0, 100000)
print(next(rand_gen))
print(next(rand_gen))

print("\n")

def range_generator(range_length):
    iterator = 0
    while iterator < range_length:
        yield iterator
        iterator += 1

range_gen = range_generator(10)
for item in range_gen:
    print(item)

print("\n")

def map_generator(func, user_list):
    iterator = 0
    list_length = len(user_list)
    while iterator < list_length:
        yield func(user_list[iterator])
        iterator += 1


map_gen = map_generator(ord, "bwbwjwjwjw")
for item in map_gen:
    print(item)

print("\n")


def enumerate_generator(user_list):
    itetator = 0
    list_length = len(user_list)
    while itetator < list_length:
        yield (itetator, user_list[itetator])
        itetator += 1

enum_gen = enumerate_generator("asdasdasdasdasd")
for item in enum_gen:
    print(item)

print("\n")

def zip_generator(list1, list2):
    iterator = 0
    list1_len = len(list1)
    list2_len = len(list2)
    while iterator < list1_len and iterator < list2_len:
        yield (list1[iterator], list2[iterator])
        iterator += 1


zip_gen = zip_generator("adadad", "bbbbb")
for item in zip_gen:
    print(item)