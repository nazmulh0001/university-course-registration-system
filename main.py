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
    
#student class
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

