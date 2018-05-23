import getCourseString


# Helper function for pruneByPrereq that asserts whether any element is satisfied
def orTrue (orPreReqsList, coursesTaken):
    for pre in orPreReqsList:

        if type(pre) is list:                               # 'OR' separated prerequisites
            if orTrue(pre):                                 # Something in 'OR' is present
                return True

        elif type(pre) is tuple:                            # 'AND' separated prerequisites
            if handleAnd(pre):                              # Everything in 'AND' is present
                return True                                 # orPreReqsList satisfies requirements

        else:
            courseStr = getCourseString(pre)
            if courseStr in coursesTakenInPlan:             # Individual prereq present
                return True                                 # Report able to qualify for this course

    return False                                            # No element in 'OR' present. Unable to qualify


# Helper function for pruneByPrereq that asserts whether all elements are satisfied
def andTrue(andPreReqsList, coursesTaken):
    for pre in andPreReqsList:

        if type(pre) is list:                               # 'OR' separated prerequisites
            if not orTrue(pre, coursesTaken):               # Nothing in 'OR' is present
                return False

        elif type(pre) is tuple:                            # 'AND' separated prerequisites
            if not andTrue(pre, coursesTaken):              # Something in 'AND' not present
                return False

        else:
            courseStr = getCourseString(pre)
            if courseStr not in coursesTakenInPlan:         # Individual prereq present
               return False                                 # Report able to qualify for this course

    return True                                             # Every element in 'AND' present. Able to qualify


# Removes courses from the query if the student cannot qualify
def pruneByPrereq (listFromQuery, coursesTaken):
    reachableCourses = ()                                   # List of lists of course info for courses the student
                                                            # qualifies for
    canReach = True

    for course in listFromQuery:                            # For each row(course info) in listFromQuery
        canReach = True                                     # Tracks whether the student has all needed prerequisites
        preReqs = course[4]                                 # Index of prereqs column of course

        for pre in preReqs:                                 # For each item in preReqs

            if type(pre) is list:                           # 'OR' separated prerequisites
                if handleOr(pre, coursesTaken) == False:
                    canReach = False
                    break

            elif type(pre) is tuple:                        # 'AND' separated prerequisites
                if andTrue(pre,coursesTaken) == False:
                    canReach = False
                    break

            else:                                           # Single prereq
                courseStr = getCourseString(pre)
                if courseStr not in coursesTaken:
                    canReach = False
                    break

        if canReach is True:                                # If all prerequisites met add course to reachableCourses
            reachableCourses.append(course)

    return reachableCourses


# Removes courses from the query results that collide with another course taken
# 'mon' 'tues' 'wed' 'thurs' 'OnLine'. Found in column 2 of results
def pruneOffDay(listFromQuery, dayToPrune):
    dayToPrune = dayToPrune.lower()
    prunedList = ()

    if dayToPrune == 'none':                                # Does not filter any courses off of the list
        return listFromQuery

    for course in listFromQuery:
        if course[2] == 'online':                           # If courses day of week is online
            prunedList.append(course)                       # Can always include online courses

        if course[2] != dayToPrune:                         # If courses day of the week isn't dayToPrune
            prunedList.append(course)

    return prunedList


# Removes courses from the query result that the student has already taken.
def pruneOffPrevCourses (listFromQuery, coursesTaken):
    prunedList = ()

    for course in listFromQuery:
        courseStr = getCourseString(pre)

        if courseStr not in coursesTaken:
            prunedList.append(course)

    return prunedList


# Removes courses from the query not present in given curriculum.
def pruneByCurriculum(listFromQuery, curriculum):
    prunedList = ()

    for course in listFromQuery:
        courseStr = getCourseString(pre)

        if courseStr in curriculum.coursesInCurriculum:
            prunedList.append(course)

    return prunedList


# Applies all filters to the original query and returns filtered list.
def filter (listFromQuery, plan, dayToPrune, curriculum):
    filter1 = pruneOffPrevCourses(listFromQuery, plan.coursesTaken)
    filter2 = pruneOffDay(filter1, dayToPrune)
    filter3 = pruneByCurriculum(filter2, curriculum)
    return pruneByPrereq(filter3, plan.coursesTaken)
