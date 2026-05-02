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