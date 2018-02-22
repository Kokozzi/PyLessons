from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello world"


@app.route("/user/<username>")
def hello_user(username):
    return "Hello, {}".format(username)


@app.route("/sum", methods=["GET"])
def sum():
    try:
        number1 = int(request.args.get("num1"))
        number2 = int(request.args.get("num2"))
        return "Result is: {}".format(number1 + number2)
    except ValueError:
        return "Params must be numbers"


@app.route("/concat", methods=["GET"])
def concat():
    try:
        str1 = str(request.args.get("str1"))
        str2 = str(request.args.get("str2"))
        return "Result is: {}".format(str1 + str2)
    except ValueError:
        return "Params must be Strings"


@app.route("/length", methods=["GET"])
def length():
    try:
        str1 = str(request.args.get("str1"))
        str2 = str(request.args.get("str2"))
        if len(str1) > len(str2):
            max_string = str1
        else:
            max_string = str2
        return "Longest string is: {}".format(max_string)
    except ValueError:
        return "Params must be Strings"


@app.route("/path/<path:file_path>")
def path_check(file_path):
    try:
        f = open(file_path)
        return "File was found"
    except FileNotFoundError:
        return "No such file"


if __name__ == "__main__":
    app.run()