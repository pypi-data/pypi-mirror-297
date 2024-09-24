import inspect
import os

class My:
    def __init__(self):
        file = inspect.stack()[1]
        self.path = os.path.dirname(file.filename)

test = My()
print(test.path)