def test_func(in_func, *args):
    print("in")
    if callable(in_func):
        in_func(*args)
    print("out")


def hello_func(a):
    print(a)
    print("hello")


def returnable_func():
    print("i was returned")


def i_wiil_return():
    return returnable_func

#test_func(hello_func, "bbb")
#i_wiil_return()()

########################
# Замыкания
#######################

def parent_func(value):
    def child_func():
        print("parent value is: ", value)
    return child_func

v = parent_func("text1234")
v()