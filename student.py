import csv

class Student:
    def __init__(self, history_file, gpa=3.0):
        self.completed_courses = self.load_history(history_file)
        self.registered_courses = []
        self.gpa = gpa

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