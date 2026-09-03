from abc import ABC, abstractmethod
class A(ABC):
    @abstractmethod
    def payment(self):
        pass

class B(A):
    def payment(self):
            print("Payment processed successfully....")
    pass
b = B()
b.payment()