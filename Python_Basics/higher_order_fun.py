def square(num):
    return num * num

def cube(num):
    return num * num * num

def c_fun(num,operation):
    return operation(num)
var = 5
print(c_fun(var,square))

