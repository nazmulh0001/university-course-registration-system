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