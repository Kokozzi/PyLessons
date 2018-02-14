from functools import wraps, reduce

# Decorator that check types of input params and inner function result
def check(input_type=None, output_type=None):
    def inner_decorator(func):
        @wraps(func)
        def inner(*args):
            # If decorator get input type for checking
            if input_type is not None:
                # Iterate over args and compare their type with required. Reduce their results into one
                if not reduce(lambda x,y: x and y, map(lambda x: isinstance(x, input_type), args)):
                    # One of args has wrong type, raise error
                    raise TypeError("Input arguments have wrong type!")
            # Call function
            result = func(*args)
            # If decorator get required type for result
            if output_type is not None:
                if not isinstance(result, output_type):
                    raise TypeError("Result has wrong type!")
            return result
        return inner
    return inner_decorator


# Check if input params are integers and function returns integer
@check(input_type=int, output_type=int)
def sum(x,y):
    result = x + y
    print(result)
    # Check wrong result type - string
    # return "a"
    return result


sum(5,1)
# Check wrong input parameter type - string
#sum("f",1)