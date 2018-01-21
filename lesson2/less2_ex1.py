# Flags for questions' loops. Finish loop when flag equal False
repeat_question_one = True
repeat_question_two = True
repeat_question_three = True
# Every key is a separate question, contains dict with question text and answers list pair
questions_and_answers = {
    "question_1": {
        "question": "The first question: What programming language do you learn?\n",
        "answers": ["python", "PYTHON", "Python"]
    },
    "question_2": {
        "question": "The second question: What is your education centre name?\n",
        "answers": ["#tceh", "tceh"]
    },
    "question_3": {
        "question": "The third question: What is the correct discription for everything in Python?\n",
        "answers": ["object", "obj", "OBJECT", "Object"]
    }
}

print("Hi! Let me ask you three questions, please.\n")

# Infinite loop until getting correct answer from user
while repeat_question_one:
    # Ask user to type answer
    language_answer = input(questions_and_answers["question_1"]["question"])
    # Compare user's answer with list of correct answers 
    if language_answer in questions_and_answers["question_1"]["answers"]:
        # Setting flag to False for breaking loop
        repeat_question_one = False
    else:
        print("Incorrect answer! Please try again.\n")

print("Nice! Heading to the next question!\n")

while repeat_question_two:
    edu_center_answer = input(questions_and_answers["question_2"]["question"])
    if edu_center_answer in questions_and_answers["question_2"]["answers"]:
        repeat_question_two = False
    else:
        print("Incorrect answer! Please try again.\n")

print("Great! Heading to the final one!\n")

while repeat_question_three:
    object_answer = input(questions_and_answers["question_3"]["question"])
    if object_answer in questions_and_answers["question_3"]["answers"]:
        repeat_question_three = False
    else:
        print("Incorrect answer! Please try again.\n")

print("Great job! Thank you and see you soon again :)")