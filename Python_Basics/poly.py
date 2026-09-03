class Laptop:
    def build(self):
        print("Build a Laptop")

class Desktop:
    def build(self):
        print("Build a Desktop")

class Tab:
    def Read_pdf(self):
        print("Reading a Book")

class Developer:
    def code(self,machine: Laptop):
        print("Developer Coding...")
        machine.build()

dell = Laptop()
apple = Desktop()
lenova = Tab()

sudheer = Developer()
sudheer.code(dell)
sudheer.code(apple)
sudheer.code(lenova)