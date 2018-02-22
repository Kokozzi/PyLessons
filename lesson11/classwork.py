from contextlib import contextmanager


@contextmanager
def do_work(value):
    print('some work before, __enter__')
    yield value
    print('some work after, __exit__')


with do_work(14) as w:
    print('Some work here!')
    print(w)


@contextmanager
def open_some_file(filename, mode="r"):
    print('some work before, __enter__')
    try:
        fd = open(filename, mode)
    except Exception as e:
        print("File not opened")
        fd = None
    yield fd
    if fd is not None:
        fd.close()
    print('some work after, __exit__')


# with open_some_file("test_file.txt", "w") as f:
#     print("enter inside")
#     if f is not None:
#         f.write("helllo")