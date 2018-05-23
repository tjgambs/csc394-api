import search
import generateOptions
import serialization

'''
This runs the degree Builder. In order the following will occur:
1. The JSON payload passed from the front end will be deserialized into a student object.
2. The option type from the student object will be checked. If it is a:
        0 - automated search
        1 - manual search
3. The option type method will be called.
4. The method will return a serialized JSON of courses

'''
def runDegree(self):
    student_object = serialization.deserializeForStudent(self)
    if student_object.option_type == 0:
        return automatedSearch(student_object)
    else:
        return manualSearch(student_object)

def automatedSearch(self):
    search.automated(self)

def manualSearch(self):
    day_to_prune = "none"
    list.append(generateOptions.generateOptions(self, day_to_prune, self.curriculum))
    results = serialization.classListSerialize(list)
    return results
