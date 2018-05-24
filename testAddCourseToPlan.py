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

jsonDump = '{"student_id": "123Test", \
    "number_of_classes_per_quarter": "1", \
    "coursesTaken": ["csc 401"], \
    "numTerm": "990", \
    "curriculum": "10", \
    "elective_preference": "5", \
    "option_type": "0"}'


#=======================================================================================================================
# Defining the CS Curriculum and testing it

intros = set(['csc 400', 'csc 401', 'csc 402', 'csc 403', 'csc 406', 'csc 407'])
foundations = set(['csc 421', 'csc 435', 'csc 447', 'csc 453', 'se 450'])
advCourses = set()
openElects = set()
softDevs = set(['csc 436', 'csc 438', 'csc 439', 'csc 443', 'csc 448', 'csc 461', 'csc 462', 'csc 471', 'csc 472', \
            'csc 475', 'csc 534', 'csc 536', 'csc 540', 'csc 548', 'csc 549', 'csc 551', 'csc 552', 'csc 553', \
            'csc 595', 'cns 450', 'gam 690', 'gam 691', 'hci 441', 'se 441', 'se 452', 'se 459', 'se 525', 'se 526', \
            'se 554', 'se 560', 'se 491', 'se 591', 'tdc 478', 'tdc 484', 'tdc 568'])
theorys = set(['csc 431', 'csc 440', 'csc 444', 'csc 489', 'csc 503', 'csc 521', 'csc 525', 'csc 531', 'csc 535', \
           'csc 547', 'csc 557', 'csc 580', 'csc 591', 'se 553'])
dataScis = set(['csc 423', 'csc 424', 'csc 433', 'csc 465', 'csc 478', 'csc 481', 'csc 482', 'csc 495', 'csc 529', \
            'csc 555', 'csc 575', 'csc 578', 'csc 594', 'csc 598', 'csc 672'])
databases = set(['csc 433', 'csc 452', 'csc 454', 'csc 478', 'csc 529', 'csc 543', 'csc 549', 'csc 551', 'csc 553', \
             'csc 554', 'csc 555', 'csc 575', 'csc 589'])
ais = set(['csc 457', 'csc 458', 'csc 478', 'csc 480', 'csc 481', 'csc 482', 'csc 495', 'csc 528', 'csc 529', 'csc 538', \
       'csc 575', 'csc 576', 'csc 577', 'csc 578', 'csc 583', 'csc 587', 'csc 592', 'csc 594', 'ect 584', 'geo 441', \
       'geo 442', 'is 467'])
softEngs = set(['se 430', 'se 433', 'se 441', 'csc 452', 'se 453', 'se 456', 'se 457', 'se 459', 'se 475', 'se 477', \
            'se 480', 'se 482', 'se 491', 'se 525', 'se 526', 'se 529', 'se 533', 'se 546', 'se 549', 'se 554', \
            'se 556', 'se 560', 'se 579', 'se 581', 'se 582', 'se 591'])
gameRTSys = set(['se 461', 'csc 462', 'csc 486', 'csc 588', 'gam 425', 'gam 450', 'gam 453', 'gam 470', 'gam 475', \
             'gam 476', 'gam 486', 'gam 575', 'gam 576', 'gam 690', 'gam 691', 'gph 436', 'gph 469', 'gph 570', \
             'gph 572', 'gph 580', 'se 456'])
humCompInts = set(['csc 436', 'csc 438', 'csc 465', 'csc 471', 'csc 472', 'csc 491', 'csc 492', 'hci 440', 'hci 441', \
               'hci 430', 'hci 454'])
capstones = set()
majElects = softDevs.union(theorys).union(dataScis).union(databases).union(ais).union(softEngs).union(gameRTSys).union(humCompInts)
courseDesignations = [intros, foundations, majElects, openElects, capstones, softDevs, theorys, dataScis, databases, ais, softEngs, gameRTSys, humCompInts, advCourses]
# Each index represents a type of course. Stores the int num of that type taken
# Indexes correspond to the following course types
# 0:  Introductory Courses
# 1:  Foundation Courses
# 2:  Major Elective Courses
# 3:  Open Elective Courses
# 4:  Capstone Courses
# 5:  Software Systems Development Courses
# 6:  Theory Courses
# 7:  Data Science Courses
# 8:  Database Systems Courses
# 9:  AI Courses
# 10: Software Engineering Courses
# 11: Game and Real-Time Systems Courses
# 12: Human-Computer Interaction Courses
# 13: Advanced Courses
coursesInCurriculum = intros.union(foundations).union(majElects).union(openElects).union(softDevs).union(theorys).union \
                           (dataScis).union(databases).union(ais).union(softEngs).union(gameRTSys).union(humCompInts).union(advCourses)
# Indexes correspond to the number of intro, foundation, major electives, open electives, capstones, courses \
# from a single concentration required for graduation, and advanced_courses
gradReqs = [6, 5, 8, 0, 0, 4, 0]

# create the curriculum from data above
csCurriculum = Curriculum(courseDesignations, gradReqs)

print('cs1:')
print(csCurriculum.introductory_courses)
'''
print('Next line should be true')
print('csc 400' in csCurriculum.introductory_courses)
print('zroc 465' in csCurriculum.coursesInCurriculum)
print(gradReqs[1])
print('se 477' in csCurriculum.coursesInCurriculum)
'''

# create the curriculum from the CS class
cs2 = defineCurriculum()
print('cs2:')
print(cs2.introductory_courses)
#=======================================================================================================================
# Create the student
the_student_obj = Student.Student("123Test", 1, ["csc 401", "csc 400"], 990, csCurriculum, 5, 0)
'''
print(the_student_obj.curriculum.ai_courses)
print(the_student_obj.coursesTaken)
'''

#=======================================================================================================================
# Run a query
# generateOptions.generateOptions(the_student_obj, 'mon', csCurriculum)
# Currently is crashing because the parsing isn't quite correct. It gets this: File "<string>", line 1
#     ['('CSC 406', CSC 402')]    It is currently missing the ' before CSC 402
