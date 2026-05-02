import csv
from course import Course

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
                        row.get('Prerequisite', "NONE"),
                        row.get('Schedule', "")
                    )
                    courses[course.code] = course
        except FileNotFoundError:
            print("Course file not found!")
        return courses

    def show_courses(self):
        print("\nAvailable Courses:")
        for course in self.courses.values():
            print(course)

    def has_conflict(self, student, new_course):
        for c in student.registered_courses:
            if c.schedule == new_course.schedule:
                return True
        return False

    def can_register(self, student, course):
        # Duplicate
        if course in student.registered_courses:
            print("Already registered this course.")
            return False

        # Already completed
        if course.code in student.completed_courses:
            print("You have already completed this course.")
            return False

        # GPA-based credit limit
        max_credits = 18 if student.gpa >= 3.75 else 15
        if student.total_credits() + course.credits > max_credits:
            print(f"Credit limit exceeded (max {max_credits}).")
            return False

        # Prerequisite
        if course.prerequisite != "NONE":
            if course.prerequisite not in student.completed_courses:
                print(f"Missing prerequisite: {course.prerequisite}")
                return False

        # Schedule conflict
        if self.has_conflict(student, course):
            print("Schedule conflict detected.")
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

    def drop_course(self, student, course_code):
        course_code = course_code.strip().upper()
        before = len(student.registered_courses)

        student.registered_courses = [
            c for c in student.registered_courses if c.code != course_code
        ]

        if len(student.registered_courses) < before:
            print("Course dropped successfully.")
        else:
            print("Course not found.")

    def recommend_courses(self, student):
        recommendations = []
        for course in self.courses.values():
            if course.code in student.completed_courses:
                continue
            if course in student.registered_courses:
                continue
            if course.prerequisite == "NONE" or course.prerequisite in student.completed_courses:
                recommendations.append(course)
        return recommendations

    def save_registration(self, student, file="registered_courses.csv"):
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Course Code", "Course Title"])
            for c in student.registered_courses:
                writer.writerow([c.code, c.title])