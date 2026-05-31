from account import BankAccount   # importing class

# creating object
name = input("Enter name: ")
amount = input("Enter amount: ")
acc1 = BankAccount(name, int(amount))

# using methods
acc1.show_balance()
depositAmount = input("Enter amount to deposit: ")
acc1.deposit(int(depositAmount))
acc1.show_balance()
withdrawAmount = input("Enter amount to withdraw: ")
acc1.withdraw(int(withdrawAmount))
acc1.show_balance()