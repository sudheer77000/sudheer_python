class Sudheer:

    def __new__(cls):
        print("This is New Method")
        return super(Sudheer,cls).__new__(cls)

    def __init__(self):
        print("This is __init__ method")
    def show(self):
        print("This is Sudheer Class")

obj1 = Sudheer.__new__(Sudheer)
obj1.show()
obj1.__init__()