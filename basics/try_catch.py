try:
    num = int(input("Enter a number: "))
    result = 100 / num
    print(result)

except ValueError:
    print("Please enter a valid number")

except ZeroDivisionError:
    print("Number cannot be zero")

else:
    print("Processed Successfully")
finally:
    print("End")