from functools import wraps

# Declaring custom Exceptions
class RightError(Exception):
    pass

class AnotherError(Exception):
    pass

class WrongError(Exception):
    pass

# Decotator for passing only RigthErrors, and replacing all others with WrongError
def error_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # Try to execute functiong
        try:
            result = func(*args, **kwargs)
            return result
        # RightError raised, pass it further
        except RightError:
            raise
        # Raised error not from RightError class, replace it with WrongError
        except:
            raise WrongError("Wrong error detected!")
    return inner

# Checking functiong with different error types
@error_decorator
def errors_rising():
    raise AnotherError("I am another type error")
    raise RightError("I am right error")

errors_rising()