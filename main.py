from student import Student
from registration_system import RegistrationSystem

def main():
    system = RegistrationSystem("course_info.csv")
    student = Student("student_history.csv", gpa=3.8)

    while True:
        print("\n========== COURSE REGISTRATION SYSTEM ==========")
        print("1. Show All Courses")
        print("2. Register Course")
        print("3. View Registered Courses")
        print("4. Exit")
        print("5. Recommend Courses")
        print("6. Drop Course")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            system.show_courses()

        elif choice == "2":
            code = input("Enter course code: ")
            system.register_course(student, code)

        elif choice == "3":
            print("\nYour Courses:")
            if not student.registered_courses:
                print("No courses registered.")
            else:
                for c in student.registered_courses:
                    print(c)
            print(f"Total Credits: {student.total_credits()}")

        elif choice == "4":
            system.save_registration(student)
            print("Saved successfully. Exiting...")
            break

        elif choice == "5":
            recs = system.recommend_courses(student)
            print("\nRecommended Courses:")
            if not recs:
                print("No available recommendations.")
            else:
                for c in recs:
                    print(c)

        elif choice == "6":
            code = input("Enter course code to drop: ")
            system.drop_course(student, code)

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()