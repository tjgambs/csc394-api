def pruneByPrereq (listFromQuery, coursesTakenInPlan):
    # TODO: refactor this as a recursive solution. Iterative is too complicated.
    reachableCourses = ()
    canReach = True

    for course in listFromQuery:                                    # Look at each row of listFromQuery
        canReach = True
        preReqs = course[5]                                         # preReqs of course. Tuples = and, list = or
        for pre in preReqs:                                         # Each item in the preReq list
            if type(pre) is tuple:                                  # Everything inside must be there to be true
                for option in pre:                                  # Look at everything inside and statement
                    if type(option) is tuple:                       # If another nested 'and' is encountered
                        for opt in option:                          # go through them
                            if opt not in coursesTakenInPlan:    # if lacking the pre req
                                canReach = False                    # report false and break out of this inner loop
                                break
                        if canReach == False:                       # break and return false since missing an and element
                            break
                    if canReach == False:                           # break and return false since missing an and element
                        break
                    elif type(option) is list:                      # must have one of these to be complete to return true
                        for opt in option:                          # Each item in this inner or statement
                            if opt in coursesTakenInPlan:           # If we meet a single pre req we can break
                                canReach = True
                                break
                            else:                                   # If the current opt isn't there mark false and continue
                                canReach = False
                        if canReach == True:                        # If we had a single true report we can break as true
                            break
                    if canReach == False:                           # If we fell through the entire 'or' without a true
                        break                                       # Break as false
                    else:
                        if option not in coursesTakenInPlan:
                            canReach = False
                            break
            elif type(pre) is list:                                 # Must include a true element of pre to return true
                for option in pre:
                    if type(option) is tuple:
                        for opt in option:
                            if opt not in coursesTakenInPlan:
                                canReach = False
                                break
                    if canReach == True:
                        break
                    if type(option) is list:
                        for opt in option:
                            if opt in coursesTakenInPlan:
                                canReach = True                     # One of the choices was there so we return true
                                break
                            else:
                                canReach = False                    # Set false if we don't satisfy the req
                        if canReach == True:                        # Did satisfy an 'or'
                            break
                    if canReach == True:
                        break
            if canReach == False:
                break
            else:
                if pre not in coursesTakenInPlan:
                    canReach = False
                    break

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