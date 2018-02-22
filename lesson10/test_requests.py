import requests

# r = requests.post('http://127.0.0.1:5000', data={"name": "name1", "email": "ab@ab.com", "job": "hr"})
r = requests.get('http://127.0.0.1:5000')
print(r.text)

cookie = r.cookies
print(cookie["guess_number"])

test_cookie = int(cookie["guess_number"]) - 1
test_cookie_2 = test_cookie + 2
test_cookie_3 = test_cookie + 1

r = requests.post("http://127.0.0.1:5000/guess", data={"guess": test_cookie}, cookies=cookie)
cookie = r.cookies
print(r.text)

r = requests.get('http://127.0.0.1:5000', cookies=cookie)
cookie = r.cookies
print(r.text)

r = requests.post("http://127.0.0.1:5000/guess", data={"guess": test_cookie_2}, cookies=cookie)
cookie = r.cookies
print(r.text)

r = requests.post("http://127.0.0.1:5000/guess", data={"guess": test_cookie_3}, cookies=cookie)
cookie = r.cookies
print(r.text)


r = requests.get('http://127.0.0.1:5000', cookies=cookie)
print(r.text)
cookie = r.cookies
print(cookie["guess_number"])