# Elements of toy list represent sticks, which is separate list
toy = [[], [], []]
steps_counter = 0

# Try to move disc from "one_stick" stick to "other_stick" or vice versa
# This params are indexes of sticks (lists in "toy" list)
def moving(one_stick, other_stick):
    # Work with global vars
    global toy
    global steps_counter
    # Tuple that represent moving rule, ex: (1,1,3)
    # Means: "Move 1st dist from 1st stick to 3rd stick"
    moving_rule = None
    if len(toy[one_stick]) == 0:
        # "One_stick" in empty, move disc here
        moving_rule = (toy[other_stick].pop(), other_stick + 1, one_stick + 1)
        toy[one_stick].append(moving_rule[0])
    elif len(toy[other_stick]) == 0:
        # "Other stick" is empty, move disc here
        moving_rule = (toy[one_stick].pop(), one_stick + 1, other_stick + 1)
        toy[other_stick].append(moving_rule[0])
    elif toy[one_stick][-1] < toy[other_stick][-1]:
        # Disc on top of other_stick is greater than disc on top of one_stick
        # Move from one_stick to other_stick
        moving_rule = (toy[one_stick].pop(), one_stick + 1, other_stick + 1)
        toy[other_stick].append(moving_rule[0])
    else:
        # Disc on top of one_stick is greater than disc on top of other_stick
        # Move from other_stick to one_stick
        moving_rule = (toy[other_stick].pop(), other_stick + 1, one_stick + 1)
        toy[one_stick].append(moving_rule[0])
    steps_counter += 1
    return moving_rule

# Ask user to input number of discs and repeat in until proper value will be inputed
while True:
    discs_count = input("Введите количество дисков: ")
    try:
        discs_count = int(discs_count)
        break
    except:
        print("Ошибка, необходимо ввести число")

pyramid_size = discs_count

# Fulling starting stick with discs in proper order
while discs_count > 0:
    toy[0].append(discs_count)
    discs_count -= 1

# Applying required scheme of moving for ODD or EVEN pyramid
if pyramid_size % 2 == 0:
    while True:
        # Repeat steps until last stick will be fulled with all discs
        if len(toy[2]) != pyramid_size:
            # Print result of moving as a tuple
            print(moving(0, 1))
        else:
            break
        if len(toy[2]) != pyramid_size:
            print(moving(0, 2))
        else:
            break
        if len(toy[2]) != pyramid_size:
            print(moving(1, 2))
        else:
            break
else:
    while True:
        if len(toy[2]) != pyramid_size:
            print(moving(0, 2))
        else:
            break
        if len(toy[2]) != pyramid_size:
            print(moving(0, 1))
        else:
            break
        if len(toy[2]) != pyramid_size:
            print(moving(1, 2))
        else:
            break

print("Шагов затрачено: {}".format(str(steps_counter)))