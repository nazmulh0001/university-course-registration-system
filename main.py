import csv

#Course Class
class Course:
    def __init__(self, code, title, credits, prerequisite):
        self.code = code
        self.title = title
        self.credits = float(credits)
        self.prerequisite = prerequisite

    def __str__(self):
        return f"{self.code} - {self.title} ({self.credits} credits) | Prereq: {self.prerequisite}"
    
#Student Class
class Student:
    def __init__(self, history_file):
        self.completed_courses = self.load_history(history_file)
        self.registered_courses = []

    def load_history(self, file):
        completed = set()
        try:
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    completed.add(row['Course Code'])
        except FileNotFoundError:
            print("History file not found. Starting fresh.")
        return completed

    def total_credits(self):
        return sum(course.credits for course in self.registered_courses)

#Registration System
class RegistrationSystem:
    def __init__(self, course_file):
        self.courses = self.load_courses(course_file)

    def load_courses(self, file):
        courses = {}
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                course = Course(
                    row['Course Code'],
                    row['Course Title'],
                    row['Credits'],
                    row['Prerequisite']
                )
                courses[course.code] = course
        return courses

    def show_courses(self):
        print("\nAvailable Courses:")
        for course in self.courses.values():
            print(course)

    def can_register(self, student, course):
        #credit limit
        if student.total_credits() + course.credits > 15:
            print("❌ Credit limit exceeded (max 15).")
            return False

        #prerequisite
        if course.prerequisite.lower() != "none":
            if course.prerequisite not in student.completed_courses:
                print(f"❌ Missing prerequisite: {course.prerequisite}")
                return False

        return True

    def register_course(self, student, course_code):
        if course_code not in self.courses:
            print("❌ Invalid course code.")
            return

        course = self.courses[course_code]

        if self.can_register(student, course):
            student.registered_courses.append(course)
            print(f"Registered: {course.title}")

#Main Program
def main():
    system = RegistrationSystem("course_info.csv")
    student = Student("student_history.csv")

    while True:
        print("\n1. Show Courses")
        print("2. Register Course")
        print("3. View Registered Courses")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            system.show_courses()

        elif choice == "2":
            code = input("Enter course code: ")
            system.register_course(student, code)

        elif choice == "3":
            print("\nYour Courses:")
            for c in student.registered_courses:
                print(c)
            print(f"Total Credits: {student.total_credits()}")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()