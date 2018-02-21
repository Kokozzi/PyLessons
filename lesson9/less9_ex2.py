import requests
import re

# Get page content from url and return it
def get_site(url):
    site = requests.get(url)
    return site.text

# Read local copy of reddit tread, saved to file
def read_file(filename):
    with open(filename, "r", encoding='utf-8') as f:
        return f.read()

# Try to open url and save it content to var
site_text = get_site("https://www.reddit.com/r/Python/comments/7ymqs7/intro_to_data_science_with_python_new_course_to/")

# Reddit connection block appeared, use local copy of thread instead
if "Too Many Requests" in site_text:
    print("Got too many requests error, use local copy\n")
    site_text = read_file("save_reddit.txt")

# Remove return symbols from page text
prepared_text = re.sub(r'\n', '', site_text)
# Find all appearances of re in page text
result = re.findall(r'data-type="comment".*?data-author="(\w+)".*?<div class="md"><p>([^<]*)</p>', prepared_text)

print("Comments:\n")
# Print results in pretty format 
for comment in result:
    print("{}: {}".format(comment[0], comment[1]))
    print()