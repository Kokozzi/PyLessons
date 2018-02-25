import datetime

class TimeContext:
    def __init__(self, func, *args, **kwargs):
        self.start_time = 0
        self.finish_time = 0
        self.func = func
        self.func_args = args
        self.func_kwargs = kwargs
    
    def __enter__(self):
        self.start_time = datetime.datetime.now()
        return self.func(*self.func_args, **self.func_kwargs)
    
    def __exit__(self, *args):
        self.finish_time = datetime.datetime.now()
        print("Elapsed time: {}".format(self.finish_time - self.start_time))


class ExceptionsContext:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.func_args = args
        self.func_kwargs = kwargs
    
    def __enter__(self):
        try:
            result = self.func(*self.func_args, **self.func_kwargs)
            return result
        except Exception:
            print("Exception appeared")
            return None
    
    def __exit__(self, *args):
        pass


def test_sum(a, b):
    return a + b


with TimeContext(test_sum, 8989889198989, 8879121114444) as result:
    print(result)

print()

with ExceptionsContext(test_sum, "error", 2) as new_result:
    if new_result is not None:
        print(new_result)