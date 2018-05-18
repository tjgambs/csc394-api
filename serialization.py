import json

def classListSerialize(classList):
    return json.dumps(classList)


def deserializeForStudent(studentInfo):
    return studentInfo