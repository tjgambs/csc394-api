import Plan
from Curriculum import Curriculum
import filterOptions
import getOptions
import generateOptions
import DegreeBuilder
import serialization
import json
from CS import defineCurriculum
import Student
import generateOptions
from class_tree import  class_list

jsonDump = '{"student_id": "123Test", \
    "number_of_classes_per_quarter": "1", \
    "coursesTaken": ["csc 401"], \
    "numTerm": "990", \
    "curriculum": "10", \
    "elective_preference": "5", \
    "option_type": "0"}'


#=======================================================================================================================
# Defining the CS Curriculum and testing it

# create the curriculum from the CS class
cs2 = defineCurriculum()
'''
print('cs2:')
print(cs2.introductory_courses)
'''
#=======================================================================================================================
# Create the student
the_student_obj = Student.Student("123Test", 1, ['csc 401', 'it 411', 'csc 455'], 990, cs2, 5, 0)
'''
print(the_student_obj.curriculum.ai_courses)
print(the_student_obj.coursesTaken)
'''

#=======================================================================================================================
# Run a query
# generateOptions.generateOptions(the_student_obj, 'mon', csCurriculum)
# Currently is crashing because the parsing isn't quite correct. It gets this: File "<string>", line 1
#     ['('CSC 406', CSC 402')]    It is currently missing the ' before CSC 402

#=======================================================================================================================
# Testing Pruning
courses = [['csc 400', 'mon', 42, []], ['csc 401', 'OnLine', 20, ['csc 400']], ['csc 444', 'tues', 10, ['csc 400', 'csc 401']], ['is 500', 'thurs', 30, [['csc 500', ('csc 400', 'csc 402')]]]]
coursesOR = [['csc 400', 'mon', 42, []], ['csc 401', 'OnLine', 20, ['csc 400']], ['csc 444', 'tues', 10, ['csc 400', 'csc 401']], ['rad 500', 'thurs', 30, [['csc 500', 'csc 400', 'csc 402']]], ['is 501', 'wed', 25, [['csc 600',['csc 700',['is 800']]]]]]
coursesAND = [['csc 400', 'mon', 42, []], ['csc 401', 'OnLine', 20, ['csc 400']], ['csc 444', 'tues', 10, ['csc 400', 'csc 401']], ['is 500', 'thurs', 30, [['csc 500', ('csc 400', ('is 300', 'csc 401'))]]]]
coursesMIX = [['csc 400', 'mon', 42, []], ['csc 401', 'OnLine', 20, [('csc 400', ['csc 401', 'is 700'])]], ['csc 444', 'tues', 10, ['csc 400', 'csc 401']], ['is 500', 'thurs', 30, [['csc 500', ('csc 400', ('is 300', 'csc 401'))]]]]
courses402 = [ ['csc 402', 'mon', 42, []], ['csc 559', 'tues', 30, []], ['csc 403', 'tues', 30, []] ]
csc452 = [['csc 452', 'tues', 20, []]]
'''
pruned_by_curriculum = filterOptions.pruneByCurriculum(coursesOR, cs2)
print (pruned_by_curriculum)
'''
'''
pruned_by_PrevCourses = filterOptions.pruneOffPrevCourses(courses, the_student_obj.coursesTaken)
print(pruned_by_PrevCourses)
'''
'''
pruned_by_prereq = filterOptions.pruneByPrereq(coursesMIX, the_student_obj.coursesTaken)
print(pruned_by_prereq)
'''
'''
pruned_by_day = filterOptions.pruneOffDay(coursesMIX, 'none')
print(pruned_by_day)
'''
cl = class_list()
preReqs1 = cl.get_prereqs('csc 402'.upper())
# print(preReqs1)
'''
removeMonFromcsc452 = filterOptions.pruneOffDay(csc452,'mon')
print('Should print csc 452: ')
print(removeMonFromcsc452)
'''
'''
#test1 = filterOptions.pruneByPrereq(csc452, the_student_obj.coursesTaken)
#print("Should be ['csc 452']: ")
#print(test1)
'''