from flask import Flask, request, make_response
import random
import os

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    if "guess_number" in request.cookies:
        guess_number = request.cookies["guess_number"]
        response = make_response("Число уже загадано")
    else:
        guess_number = random.randint(0,100)
        response = make_response("Число загадано")
    print(guess_number)

    response.set_cookie('guess_number', str(guess_number))
    return response
        

@app.route('/guess', methods=["POST"])
def guess():
    if "guess_number" in request.cookies:
        guess_number = int(request.cookies["guess_number"])
    else:
        return "Число еще не было загадано"
    current_guess = int(request.form["guess"])
    if current_guess > guess_number:
        resp_symbol = ">"
    elif current_guess < guess_number:
        resp_symbol = "<"
    else:
        resp_symbol = "="
    response = make_response(resp_symbol)
    if resp_symbol != "=":
        response.set_cookie('guess_number', str(guess_number))
    return response    


if __name__ == '__main__':
    app.run()
    random_seed = os.environ("FLASK_RANDOM_SEED")
    random.seed(random_seed)