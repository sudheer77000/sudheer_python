a = int(input("Enter Num 1 Value : "))
b = int(input("Enter Num 2 Value : "))
try:
    print(a/b)
except ZeroDivisionError as e:
    print("Zero Division Error : ",e)
except ValueError as e:
    print("Please Enter Integers : ",e)
except Exception as e:
    print("Exception : ",e)
finally:
    print("Resources Closed...")

print("Program Ends")