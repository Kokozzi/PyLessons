import datetime
from functools import wraps, reduce

# Decorator that can be enabled and disabled with help of `enabled` parameter
def switching_decorator(enabled=True):
    # Decorator for time calculation
    def time_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            # Check if parent decorator is enabled
            if enabled:
                # Print decorator name
                print("My name is:", time_decorator.__name__)
                # Save time when function was started
                start_time = datetime.datetime.now()
                # print("Start time: ", start_time)
                result = func(*args, **kwargs)
                finish_time = datetime.datetime.now()
                # print("Finish time: ", finish_time)
                # Calculate elapsed time after function was finished
                print("Elapsed time: ", finish_time - start_time)
            else:
                # If decorator is disabled - just run inner function
                result = func(*args, **kwargs)
            return result
        return inner
    return time_decorator

# Decorator for displaying name
def second_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print("My name is:", second_decorator.__name__)
        result = func(*args, **kwargs)
        return result
    return inner

# Another decorator for displaying name
def third_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print("My name is:", third_decorator.__name__)
        result = func(*args, **kwargs)
        return result
    return inner


'''
Massive decorators for displaying names and time calculation
To disable first decotator use `enabled=False` parameter
'''
@switching_decorator()
@second_decorator
@third_decorator
def palindrome_check(test_string):
    '''
    Check if string is palindrome
    Make all leters lower and remove witespaces, after that enumerate each letter, ex: [(0, 'a'), (1, 'b')]
    '''
    prepared_string = list(enumerate(filter(lambda x: x != " ", test_string.lower())))
    '''
    Consecutive compare letter with letter at the other side of string.
    For string with len == 20 compare string[0] with string[19], string[1] with string[18], etc.
    After thar - reduce result of all compares with help of `and` operator and return result
    '''
    return reduce(lambda x,y: x and y, map(lambda y: y[1] == list(filter(lambda x: x[0] == len(prepared_string) - 1 - y[0], prepared_string))[0][1], prepared_string))

# Run checking function
if palindrome_check("А роза упала на лапу Азора"):
    print("Палиндром!")
else:
    print("Не палиндром")
