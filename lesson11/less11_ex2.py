import datetime

# Measuring elapsing time
class TimeMeasureContext:
    def __init__(self):
        # Class attributes for storing start and finish time
        self.start_time = 0
        self.finish_time = 0
    # Detect start time and store it
    def __enter__(self):
        self.start_time = datetime.datetime.now()
    # Code execution is finished, detect finish time
    def __exit__(self, *args):
        self.finish_time = datetime.datetime.now()
        # Calculate result calculations time
        print("Elapsed time: {}".format(self.finish_time - self.start_time))

# Supress all exceptions
class ExceptionsContext:
    def __init__(self):
        pass
    def __enter__(self):
        pass
    # Detect raised exceptions and supress them
    def __exit__(self, exception_type, exception_value, exception__traceback):
        # If `exception_type` is present - exception was rised during code execution
        if exception_type is not None:
            # Print some info about supressed exception
            print("Exception was supressed: {}".format(exception_value))
            # Supress exception
            return True


# Time Measuring with help of context manager
with TimeMeasureContext():
    # Some example calculations
    i = 0
    while i < 10000:
        i += 1
    print("Count complete")

print()

# Exceptions supressing with help of context manager
with ExceptionsContext():
    a = 5 / 0
