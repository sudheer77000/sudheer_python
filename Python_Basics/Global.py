a = 10
def change():
    global a
    a = 15
    print("Inside : ",a)

change()
print("Outside : ",a)
