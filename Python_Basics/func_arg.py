def nam_con(f_name,l_name,**lwlargs):
   print("Other Args ",lwlargs)
   return f_name + " " + l_name
   

fname = input("Enter First Name : ")
lname = input("Enter Last Name : ")

print("Full Name : ",nam_con(f_name=fname,l_name =lname,mobile="9550714814",loc="Dubai"))
print("Full Name : ",nam_con(f_name=fname,l_name =lname))

def add(*nums):
    sum = 0
    for i in nums:
        sum += i
    return sum

print(add(1,2,3,4,6,7,8))