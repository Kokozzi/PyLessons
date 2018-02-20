import requests

def get_site(url):
    site = requests.get(url)
    print(site.text)

def read_file(filename):
    with open(filename) as f:
        return f.read()

# get_site("https://www.reddit.com/r/Python/comments/7ymqs7/intro_to_data_science_with_python_new_course_to/")

reddit_file = read_file("./lesson9/reddit.txt")

