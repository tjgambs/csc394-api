import json
from Student import Student

# This will serialize the list  or (list of list) of classes that will be returned to the front end.
def classListSerialize(classList):
    return json.dumps(classList)

# This takes a JSON payload and will create a Student object which the API will be able to use.
def deserializeForStudent(studentInfo):
    print("DE-SERIALIZING.......")
    data = json.loads(studentInfo)
    student_object = Student(data['student_id'], data['number_of_classes_per_quarter'], data['courses_taken']\
        , data['current_quarter'], data['curriculum'], data['elective_preference'], data['option_type'])
    return student_object


