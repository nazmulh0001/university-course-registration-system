class Course:
    def __init__(self, code, title, credits, prerequisite, schedule):
        self.code = code.strip().upper()
        self.title = title.strip()
        self.credits = float(credits)
        self.prerequisite = prerequisite.strip().upper() if prerequisite else "NONE"
        self.schedule = schedule.strip()

    def __str__(self):
        return f"{self.code} - {self.title} ({self.credits} credits) | {self.schedule} | Prereq: {self.prerequisite}"