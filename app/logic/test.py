from Queue import PriorityQueue
from app.logic.Plan import Plan
from app.logic.Curriculum import Curriculum
from app.models.term_courses import TermCourses
from app.logic.filterOptions import filter
from app.logic.CS import defineCurriculum

current = Plan([], set(), 1005, 2)
curriculum = defineCurriculum()
print(curriculum.courseTypeDesignations[1])

queryResults = TermCourses.getOptions(current.termNum)
filteredResults = filter(queryResults, current, 'none', curriculum)
numToKeep = 4
kept = []
'''
for i in range (0, numToKeep):
    kept.append(filteredResults[i])

for courseInfo in kept:
    print("============================")
    if courseInfo.getName not in current.coursesTaken:
        current.addCourse(courseInfo)
    print("TermIdx: " + str(current.currTermIdx))
    print(current.selectionOrder)
    print("TermNum = " + str(current.termNum))
    print("============================")

print(current.daysFilled)
'''

print("Goal Test: ")
typesTaken
print()

for j in range(0,10):

    queryResults = TermCourses.getOptions(current.termNum)
    filteredResults = filter(queryResults, current, current.daysFilled, curriculum)

    kept = []
    for i in range (0, numToKeep):
        kept.append(filteredResults[i])

    for courseInfo in kept:
        print("============================")
        if courseInfo.getName not in current.coursesTaken:
            current.addCourse(courseInfo)
            courseTypes = current.classifyCourse(courseInfo,curriculum)
            current.incrCourseType(courseTypes,current.typesTaken,curriculum.gradReqs)
        print("TermIdx: " + str(current.currTermIdx))
        print(current.selectionOrder)
        print("Course Score: " + str(courseInfo.score))
        print("TermNum = " + str(current.termNum))
        print("TypesTaken: ")
        for i in range (0, len(current.typesTaken)):
            print(current.typesTaken[i])
        print("============================")

    print(current.daysFilled)