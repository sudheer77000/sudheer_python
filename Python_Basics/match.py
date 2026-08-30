num = int(input("Enter a Number : "))
match num:
    case 1:
        print("Number is One")
    case 2:
        print("Number is Two")
    case 3:
        print("Number is Three")
    case 4:
        print("Number is Four")
    case _:
        print("Incorrect")