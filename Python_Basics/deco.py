
def big_first(func):
    def bigfir(num1,num2):
        if num1 < num2:
           num1,num2 = num2,num1
           return func(num1,num2)
    return bigfir

def log_def(func):
    def log(num1,num2):
        print("Number 1 : ",num1)
        print("Number 2 : ",num2)
        return func(num1,num2)
    return log
@big_first
@log_def
def sub(num1, num2):
    return num1 - num2

@log_def
@big_first
def div(num1,num2):
    return num1/num2


print(div(2,4))
print(sub(2,4))