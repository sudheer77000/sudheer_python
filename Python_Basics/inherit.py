class A:
    def __init__(self):
        print("Init Method of Class A")
    def a1(self):
        print("Class A, a1 Method")

class B(A):

    def __init__(self):
        super().__init__()
        print("Init Method of Class B")

    def b1(self):
        super().a1()
        print("Class B, b1 Method")

obj_b = B()
obj_b.b1()