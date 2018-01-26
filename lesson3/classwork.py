from random import randint

def exceptions_func():
    pointer = randint(0,2)
    if pointer == 0:
        raise ValueError("ValueError raised")
    elif pointer == 1:
        raise TypeError("TypeError raised")
    else:
        raise RuntimeError("RuntimeError raised")


def sorting_func(sorting_list):
    for element in sorting_list:
        if not isinstance(element, int):
            raise ValueError("Not INT element detected")
    return sorted(sorting_list)


def dict_keys_stringify_func(original_dict):
    updated_dict = {}
    for key, v in original_dict.items():
        if isinstance(key, str):
            updated_dict[key] = v
           # .update({key: original_dict[key]})
        else:
            updated_dict[str(key)] = v
            # .update({str(key): original_dict[key]})
    return updated_dict


def numbers_multiplier_func(*args):
    result = 1
    for element in args:
        result *= element
    return result


try:
    exceptions_func()
except ValueError as error_text:
    print(error_text)
except TypeError as error_text:
    print(error_text)
except RuntimeError as error_text:
    print(error_text)


try:
    new_list = sorting_func([6, 1, 5, 10])
    print(new_list)
except ValueError as error_text:
    print(error_text)

try:
    new_list2 = sorting_func([6, 1, 5, "a"])
    print(new_list2)
except ValueError as error_text:
    print(error_text)

example_dict = {1: "a", 2: "2", "b": "nnn"}
edited_dict = dict_keys_stringify_func(example_dict)
print(edited_dict)

print(numbers_multiplier_func(1, 5, 6, 12, 9))


try:
    x = len(5)
except TypeError as error_text:
    print("Error detected")
    import traceback
    print(traceback.format_exc())
finally:
    print("FINAL!")