import getCourseStr as gCS


# Helper function for pruneByPrereq that asserts whether any element is satisfied
def orTrue (orPreReqs, coursesTaken):
    preReqs = orPreReqs

    for i in range (len(preReqs)):

        if type(preReqs[i]) is list:                            # 'OR' separated prerequisites
            if orTrue(preReqs[i]):                              # Something in 'OR' is present
                print ("found a list in OR")
                return True

        elif type(preReqs[i]) is tuple:                         # 'AND' separated prerequisites
            if andTrue(preReqs[i]):                             # Everything in 'AND' is present
                print("found a tuple in OR")
                return True                                     # orPreReqsList satisfies requirements

        else:
            courseStr = gCS.getCourseStr(preReqs[i])
            if courseStr in coursesTaken:                       # Individual prereq present
                print("Found a course in OR")
                return True                                     # Report able to qualify for this course

    return False                                                # No element in 'OR' present. Unable to qualify


# Helper function for pruneByPrereq that asserts whether all elements are satisfied
def andTrue(andPreReqs, coursesTaken):
    preReqs = andPreReqs

    for i in range (len(preReqs)):                              # For each element in preReqs

        if type(preReqs[i]) is list:                            # 'OR' separated prerequisites
            if not orTrue(preReqs[i], coursesTaken):            # Nothing in 'OR' is present
                print("found a list in AND")
                return False

        elif type(preReqs[i]) is tuple:                         # 'AND' separated prerequisites
            if not andTrue(preReqs[i], coursesTaken):           # Something in 'AND' not present
                print("found a tuple in AND")
                return False

        else:
            courseStr = gCS.getCourseStr(preReqs[i])
            if courseStr not in coursesTaken:                   # Individual prereq present
                print("found a class in AND")
                return False                                    # Report able to qualify for this course

    return True                                                 # Every element in 'AND' present. Able to qualify


# Removes courses from the query if the student cannot qualify
def pruneByPrereq (listFromQuery, coursesTaken):
    reachableCourses = list()                                   # List of lists of course info the student qualifies for
    canReach = True

    for course in range(len(listFromQuery)):                    # For each row(course info) in listFromQuery
        canReach = True                                         # Tracks if the student has all needed prerequisites
        row = listFromQuery[course]
        preReqs = list()
        if row[3] != None:
            preReqs = row[3]                                    # Index of prereqs column of course

        if type(preReqs) != list():
            for pre in range(len(preReqs)):                     # For each item in preReqs
                print(preReqs[pre])
                if type(preReqs[pre]) is list:                  # 'OR' separated prerequisites
                    if not orTrue(preReqs[pre], coursesTaken):
                        canReach = False
                        break

                elif type(preReqs[pre]) is tuple:               # 'AND' separated prerequisites
                    if not andTrue(preReqs[pre], coursesTaken):
                        canReach = False
                        break

                else:  # Single prereq
                    #courseStr = gCS.getCourseStr(preReqs[pre])
                    if preReqs[pre] not in coursesTaken:
                        canReach = False
                        break


        if canReach is True:                                    # If all prerequisites met add course to
            reachableCourses.append(listFromQuery[course])      # reachableCourses

    return reachableCourses


# Removes courses from the query results that collide with another course taken
# 'mon' 'tues' 'wed' 'thurs' 'OnLine'. Found in column 2 of results
def pruneOffDay(listFromQuery, dayToPrune):
    dayToPrune = dayToPrune.lower()
    prunedList = ()

    if dayToPrune == 'none':                                    # Does not filter any courses off of the list
        return listFromQuery

    for course in range (len(listFromQuery)):
        if course[2] == 'online':                               # If courses day of week is online
            prunedList.append(listFromQuery[course])            # Can always include online courses

        if course[2] != dayToPrune:                             # If courses day of the week isn't dayToPrune
            prunedList.append(listFromQuery[course])

    return prunedList


# Removes courses from the query result that the student has already taken.
def pruneOffPrevCourses (listFromQuery, coursesTaken):
    prunedList = list()

    for course in range (len(listFromQuery)):
        courseStr = gCS.getCourseStr(listFromQuery[course])

        if courseStr not in coursesTaken:
            prunedList.append(listFromQuery[course])

    return prunedList


# Removes courses from the query not present in given curriculum.
def pruneByCurriculum(listFromQuery, curriculum):
    prunedList = list()

    for course in len(listFromQuery):
        courseStr = gCS.getCourseStr(listFromQuery[course])

        if courseStr in curriculum.coursesInCurriculum:
            prunedList.append(listFromQuery[course])

    return prunedList


# Applies all filters to the original query and returns filtered list.
def filter (listFromQuery, plan, dayToPrune, curriculum):
    filter1 = pruneOffPrevCourses(listFromQuery, plan.coursesTaken)
    filter2 = pruneOffDay(filter1, dayToPrune)
    #filter3 = pruneByCurriculum(filter2, curriculum)
    #return pruneByPrereq(filter3, plan.coursesTaken)
    return pruneByPrereq(filter2, plan.coursesTaken) # delete me
