import itertools
class Student:
    counter = itertools.count(start=1, step=1)
    def __init__(self,Name,Grade,Section):
        self.Name = Name
        self.Grade = Grade
        self.Section = Section
        self.id = 'CHS' + str(next(Student.counter))
    
    def display(self):
        print("===============Student details:=================")
        print("ID : ", self.id)
        print("Name : ", self.Name)
        print("Grade : ", self.Grade)
        print("Section: ", self.Section)
