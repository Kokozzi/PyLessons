from functools import wraps

# Caching decorator
def cached(func):
    # Store function call parameters and result as tuples (param1, param2, result) in list
    cached_results = []
    @wraps(func)
    def inner(number1, number2):
        # Filter cache trying to find result for this parameters
        searched_cache = list(filter(lambda x: x[0] == number1 and x[1] == number2, cached_results))
        # Case when nothing was found
        if len(searched_cache) == 0:
            # Call function
            result = func(number1, number2)
            # Store result in caching list
            cached_results.append((number1, number2, result))
        else:
            # Get result from cache without calling function
            result = searched_cache[0][2]
            print("Cached result:", result)
        return result
    return inner

# Simple summing function, sum two numbers
@cached
def sum(x, y):
    result = x + y
    print("Function called, result:", result)
    return result

# Function called, no cache found
sum(5,1)
sum(8,2)
# Params already appeared, get result from cache
sum(5,1)
sum(5,1)
sum(8,2)
# New params, function called
sum(5,3)