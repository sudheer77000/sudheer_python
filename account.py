class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount
        print(f"{amount} deposited")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"{amount} withdrawn")
        else:
            print("Insufficient balance")

    def show_balance(self):
        print(f"{self.name} Balance: {self.__balance}")