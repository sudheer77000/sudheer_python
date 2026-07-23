from Students import Student
students = [] 
while True:
    print("\nWelcome to the Student Management System")
    print("Please select an option:")
    print("1. Add a student")
    print("2. All Student details By Grade")
    print("3. Student details by ID")
    print("4. Exit")

    option = input("Enter your option: ")

    if option == "1":
        print("\nPlease enter the student details:")
        Name = input("Name: ")
        Grade = input("Grade: ")
        Section = input("Section: ")

        stu = Student(Name, Grade, Section)
        students.append(stu)
        stu.display()

    elif option == "2":
        try:
            if not students:
                raise NameError("No student found. Please add a student first.")
            else:
                grade = input("Enter the grade to search for: ")
            for stu in students:                
                if stu.Grade == grade:
                    stu.display()
        except NameError:
            print("No student found. Please add a student first.")

    elif option == "3":
        student_id = input("Enter the student ID: ")
        for stu in students:
            if stu.id == student_id:
                stu.display()
                break
        else:
            print("Student not found.")

    elif option == "4":
        print("Exiting program... Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")