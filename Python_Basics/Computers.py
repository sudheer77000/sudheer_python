class Computers:
    brand = "Sudheer-Gundra"

    def __init__(self,cpu,ram,ssd):
        print("Init Method Called")
        self.cpu = cpu
        self.ram = ram
        self.ssd = ssd

    @classmethod
    def info(cls):
        return cls.brand

    @staticmethod
    def getName(name) -> int:
        return name

com1 = Computers('i5','24GB','512GB')
com2 = Computers('i7','32GB','1024GB')
com3 = Computers('i9','64GB','2048GB')

print(Computers.brand)
print(Computers.info())
print(Computers.getName("Sudheer"))

var1 = 'Honey'
var2 = None

test = var2 or var1
print(test)


