s = [1, 2, 3, 4, 5]
a = [el * 2 for el in s]
print(a)
b = [el for el in s if el % 2 == 0]
print(b)


gen_list = list(map(lambda x: x + 1 ,s))
print(gen_list)

filter_list = list(filter(lambda x: x > 2, s))
print(filter_list)

from functools import reduce

reduce_list = reduce(lambda x, y: x + y, s)
print(reduce_list)

test_str = "ыфвлдшщзуйцтстршвоылфщшоуйцююб"

if len(list(filter(lambda x: x not in test_str, list(map(chr, list(range(ord("а"), ord("я") + 1))))))) == 0:
    print("Pangram")
else:
    print("Not pangram")