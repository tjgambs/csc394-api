def pruneByPrereq (listFromQuery, coursesTakenInPlan):
    reachableCourses = ()
    canReach = True

    for course in listFromQuery:
        canReach = True
        preReqs = course[5]
        for pre in preReqs:
            if type(pre) is list:
                for prereqOptions in pre:
                    if pre not in coursesTakenInPlan:
                        canReach = False
            else:
                if pre not in coursesTakenInPlan:
                    canReach = False

        if canReach is True:
            reachableCourses.append(course)
    return reachableCourses


# Removes courses from the query results that collide with another course taken
# 'mon' 'tues' 'wed' 'thurs' 'OnLine'
def pruneOffDay(listFromQuery, dayToPrune):
    prunedList = ()
    for course in listFromQuery:
        if course[indexOfDay] != dayToPrune:        #TODO: indexOfDay will be from the database
            prunedList.append(course)
    return prunedList


# Removes courses from the query result that the student has already taken.
def pruneOffPrevCourses (listFromQuery, coursesTakenInPlan):
    prunedList = ()
    for course in listFromQuery:
        if course[indexOfCourseID] not in coursesTakenInPlan:
            prunedList.append(course)
    return prunedList


def pruneByCurriculum(listFromQuery, curriculum):
    prunedList = ()
    for course in listFromQuery:
        if course in curriculum.coursesInCurriculum:
            prunedList.append(course)
    return prunedList


def filterQuery (listFromQuery, plan, dayToPrune, curriculum):
    filter1 = pruneOffPrevCourses(listFromQuery, plan.coursesTaken)
    filter2 = pruneOffDay(filter1, dayToPrune)
    filter3 = pruneByCurriculum(filter2, curriculum)
    return pruneByPrereq(filter3, plan.coursesTaken)