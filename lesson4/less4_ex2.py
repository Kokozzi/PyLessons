from random import sample

# Sorting pair of lists
def lists_sort(list1, list2):
    # Result list, combined of inputed pair
    new_list = []
    # Detect lengths of inputed lists
    list1_len = len(list1)
    list2_len = len(list2)
    # Create iterators for inputed lists
    list1_iterator, list2_iterator = 0, 0
    # Iterate till the end of one list
    while list1_iterator != list1_len and list2_iterator != list2_len:
        # Get elements of lists at iterator positions and compare them
        # Min of this elements appends to result list, after that - increment iterator for parent list of min element
        if list1[list1_iterator] < list2[list2_iterator]:
            new_list.append(list1[list1_iterator])
            list1_iterator += 1
        else:
            new_list.append(list2[list2_iterator])
            list2_iterator += 1
    # Append "tail" elements of that list, which end was not reached, to the result
    if list1_iterator == list1_len:
        new_list += list2[list2_iterator:]
    else:
        new_list += list1[list1_iterator:]
    return new_list


# Recursive function that splits list into two parts and calls sorting function for them
def recursion_sorting(numbers_list):
    list_len = len(numbers_list)
    # Terminate recursion if list contains only one element
    if list_len == 1:
        return numbers_list
    # Split list into halfs (first part will be larger for lists with odd number of elements)
    half = list_len // 2 + list_len % 2
    # Recursive calling of list splitting and sorting for each pair
    return lists_sort(recursion_sorting(numbers_list[:half]), recursion_sorting(numbers_list[half:]))


incorrect_input = True
# Getting list length from user
while incorrect_input:
    list_len = input("Введите размер списка (он будет наполнен числами в случайном порядке):")
    try:
        list_len = int(list_len)
        incorrect_input = False
    except ValueError:
        print("Ошибка! Пожалуйста, введите целое число")

# Generate list of random numbers with requested length
numbers_list = sample(range(list_len), k=list_len)
print("Случайный список:\n", numbers_list)
# Start recursive sorting
result = recursion_sorting(numbers_list)
print("Отсортированный список:\n", result)