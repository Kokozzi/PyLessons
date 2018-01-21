user_input_value = None # Stores user input chars, updates at each step
calc_result = None # Intermediate calculations result
input_number = None # Stores last number user inputed
input_operator = None # Stores last operator user inputed
possible_operators = ["+", "-", "*", "/"] 
user_input_counter = 1 # Counts each succesfull input for providing correct number/operator input order

print("\nWelcome to the brand new calculator!\nPossible operations: +, -, *, / \nPress Enter to exit \n")

# Infinite loop, breaks when user inputs empty string (presses Enter)
while True:
    # Check if input counter is ODD or EVEN. ODD counter means that number is required. EVEN counter - operation symbol 
    if user_input_counter % 2 != 0:
        user_input_value = input("Input number:\n")
    else:
        user_input_value = input("Input operation symbol:\n")

    # Check user input for empty string. Break "while" loop and close calculator if empty input is detected
    if user_input_value == "":
        # Calc_result will not be None if user already inputed some numbers or operations
        if calc_result != None:
            print("Final result: %g \nClosing calculator" % calc_result)
            break
        else:
            print("Closing calculator")
            break
    else:
        if user_input_counter % 2 != 0:
            # ODD step - get number from user and check if it is really number. In case of error - asking for new input
            try:
                input_number = float(user_input_value)
                # First number from user passes to calculation result.
                # Otherwise - check current inputed operator and make calculations over intermediate result and current inputed number
                if user_input_counter == 1:
                    calc_result = input_number
                elif input_operator == "+":
                    calc_result = calc_result + input_number
                elif input_operator == "-":
                    calc_result = calc_result - input_number
                elif input_operator == "*":
                    calc_result = calc_result * input_number
                elif input_operator == "/":
                    calc_result = calc_result / input_number
                else:
                    print("Error! Incorrect operator detected.\n")
                    break
                # Print intermediate result if some calculations were already done
                if user_input_counter > 1:
                    print("Intermediate result: %g \n" % calc_result)
                # Increment steps counter in case of succesfull number input
                user_input_counter = user_input_counter + 1
            except ValueError:
                # Display error and return to the beginning of "while" infinite loop
                print("Incorrect character detected!\n")
                continue
        else:
            # EVEN step - get operator from user and check if it belongs to possible operators list
            if user_input_value in possible_operators:
                # Rewrite current operator var with new input. Will be used during calculations at ODD step
                input_operator = user_input_value
                # Increment steps counter in case of succesfull operator input
                user_input_counter = user_input_counter + 1
            else:
                # Display error and return to the beginning of "while" infinite loop
                print("Incorrect operation symbol! Possible operations: +, -, *, / \n")
                continue
