from pathlib import Path
import sys

print("Python Basics")


class Basic:
    """This is My Basic Python Class"""

    count = 0

    def __init__(self):
        print("Object created")

    def hello(self):
        print("Hello")

    @classmethod
    def show_count(cls):
        print(cls.count)

print(Basic.__doc__)
basicObj = Basic()
basicObj.hello()
Basic.show_count()
Basic.hello(basicObj)