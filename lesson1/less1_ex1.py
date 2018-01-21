# Flags for questions' loops. Finish loop when flag equal False
repeat_question_one = True
repeat_question_two = True
repeat_question_three = True

print("Hi! Let me ask you three questions, please.\n")

# Infinite loop until getting correct answer from user
while repeat_question_one:
    # Ask user to type answer
    language_answer = input("The first question: What programming language do you learn?\n")
    # Compare user's answer in lower case with correct answer
    if language_answer.lower() == "python":
        # Setting flag to False for breaking loop
        repeat_question_one = False
    else:
        print("Incorrect answer! Please try again.\n")

print("Nice! Heading to the next question!\n")

while repeat_question_two:
    edu_center_answer = input("The second question: What is your educational center name?\n")
    if edu_center_answer.lower() == "#tceh":
        repeat_question_two = False
    else:
        print("Incorrect answer! Please try again.\n")

print("Great! Heading to the final one!\n")

while repeat_question_three:
    object_answer = input("The third question: What is the correct discription for everything in Python?\n")
    if object_answer.lower() == "object":
        repeat_question_three = False
    else:
        print("Incorrect answer! Please try again.\n")

print("Great job! Thank you and see you soon again :)")