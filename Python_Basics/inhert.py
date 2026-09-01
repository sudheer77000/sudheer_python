class A:
    var_A = 10
    def a_1(self):
        print("Method Name : a_1")
    def a_2(self):
        print("Method Name : a_2")
    def parent(self):
        print("Class A Method : parent")

class B:
    def b_1(self):
        print("Method Name : b_1")
    def b_2(self):
        print("Method Name : b_2")
    def parent(self):
        print("Class B Method : parent")

class C(B,A):
    def c_1(self):
        print("Method Name : c_1")
    def c_2(self):
        print("Method Name : c_2")
    #def parent(self):
    #    print("Class C Method : parent")

obj_c = C()
obj_c.parent()