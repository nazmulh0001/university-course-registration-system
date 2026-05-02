import csv
from registration_system import RegistrationSystem


# Course Class
class Course:
    def __init__(self, code, title, credits, prerequisite):
        self.code = code.strip().upper()
        self.title = title.strip()
        self.credits = float(credits)
        self.prerequisite = prerequisite.strip().upper() if prerequisite else "NONE"

    def __str__(self):
        return f"{self.code} - {self.title} ({self.credits} credits) | Prereq: {self.prerequisite}"


# Student Class
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
                    completed.add(row['Course Code'].strip().upper())
        except FileNotFoundError:
            print("History file not found. Starting fresh.")
        return completed

    def total_credits(self):
        return sum(course.credits for course in self.registered_courses)


# Registration System
class RegistrationSystem:
    def __init__(self, course_file):
        self.courses = self.load_courses(course_file)

    def load_courses(self, file):
        courses = {}
        try:
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    course = Course(
                        row['Course Code'],
                        row['Course Title'],
                        row['Credits'],
                        row.get('Prerequisite', "NONE")
                    )
                    courses[course.code] = course
        except FileNotFoundError:
            print("Course file not found!")
        return courses

    def show_courses(self):
        print("\nAvailable Courses:")
        for course in self.courses.values():
            print(course)

    def can_register(self, student, course):
        # Prevent duplicate registration
        if course in student.registered_courses:
            print("Already registered this course.")
            return False

        # Prevent re-taking completed course
        if course.code in student.completed_courses:
            print("You have already completed this course.")
            return False

        # Credit limit
        if student.total_credits() + course.credits > 15:
            print("Credit limit exceeded (max 15).")
            return False

        # Prerequisite check
        if course.prerequisite != "NONE":
            if course.prerequisite not in student.completed_courses:
                print(f"Missing prerequisite: {course.prerequisite}")
                return False

        return True

    def register_course(self, student, course_code):
        course_code = course_code.strip().upper()

        if course_code not in self.courses:
            print("Invalid course code.")
            return

        course = self.courses[course_code]

        if self.can_register(student, course):
            student.registered_courses.append(course)
            print(f"Registered: {course.title}")
    def recommend_courses(self, student):
        recommendations = []
        for course in self.courses.values():
            if course.code in student.completed_courses:
                continue
            if course in student.registered_courses:
                continue
            if course.prerequisite == "none" or course.prerequisite in student.completed_courses:
                recommendations.append(course)
        return recommendations


# Main Program
def main():
    system = RegistrationSystem("course_info.csv")
    student = Student("student_history.csv")

    while True:
        print("\nHello, Welcome to our course registration system!!")
        print("1. Show All Courses")
        print("2. Register Course")
        print("3. View Registered Courses")
        print("4. Exit")
        print("5. Recommend Courses")

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
            print("Thanks for using...")
            break
        elif choice == "5":
            recs = system.recommend_courses(student)
            print("\nRecommended Courses:")
            if not recs:
                print("No available recommendations.")
        else:
            for c in recs:
                print(c)
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()