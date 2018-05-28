from app.logic import serialization
from app.logic import Student

jsonDump = {"student_id": "123Test", \
    "number_of_classes_per_quarter": "1", \
    "coursesTaken": ["csc 401"], \
    "numTerm": "990", \
    "curriculum": "10", \
    "elective_preference": "5", \
    "option_type": "0"}

id = jsonDump['student_id']

the_Student = Student()
the_Student.student_id = jsonDump['student_id']

print(the_Student.student_id)