import getCourseStr as gCS


# =====================================================================================================================
# Filter potential courses leaving only courses whose prerequisites are met

# Converts prerequisite string into Strings, Tuples, and Lists for use in the prerequisite filter
# Thank you Anthony

#  TODO: Erik has a function that does this already replace this with it
def parseString(string):
    new_string = ''
    old_i = ''
    for i in string:
        if i == ',':
            new_string += '\''
        if i in '])':
            if old_i not in '[()]':
                new_string += '\''
        new_string += i
        if i in '[(':
            new_string += '\''
        old_i = i
    return eval(new_string)


# Helper function for pruneByPrereq that asserts whether any element is satisfied
def orTrue (orPreReqs, coursesTaken):
    preReqs = orPreReqs

    for i in range (len(preReqs)):

        if type(preReqs[i]) is list:                            # 'OR' separated prerequisites
            if orTrue(preReqs[i]):                              # Something in 'OR' is present
                return True                                     # orPreReqs satisfies requirements

        elif type(preReqs[i]) is tuple:                         # 'AND' separated prerequisites
            if andTrue(preReqs[i]):                             # Everything in 'AND' is present
                return True                                     # orPreReqs satisfies requirements

        else:
            courseStr = gCS.getCourseStr(preReqs[i])
            if courseStr in coursesTaken:                       # Individual prereq present
                return True                                     # Report able to qualify for this course

    return False                                                # No element in 'OR' present. Unable to qualify


# Helper function for pruneByPrereq that asserts whether all elements are satisfied
def andTrue(andPreReqs, coursesTaken):
    preReqs = andPreReqs

    for i in range (len(preReqs)):                              # For each element in preReqs

        if type(preReqs[i]) is list:                            # 'OR' separated prerequisites
            if not orTrue(preReqs[i], coursesTaken):            # Nothing in 'OR' is present
                return False                                    # andPreReqs doesn't satisfy requirements

        elif type(preReqs[i]) is tuple:                         # 'AND' separated prerequisites
            if not andTrue(preReqs[i], coursesTaken):           # Something in 'AND' not present
                return False                                    # andPreReqs doesn't satisfy requirements

        else:
            courseStr = gCS.getCourseStr(preReqs[i])
            if courseStr not in coursesTaken:                   # Individual prereq present
                return False                                    # Report able to qualify for this course

    return True                                                 # Every element in 'AND' present. Able to qualify


# Removes courses from the query if the student cannot qualify
def pruneByPrereq (listFromQuery, coursesTaken):
    reachableCourses = list()                                   # List of lists of course info the student qualifies for
    canReach = True                                             # Default assumption

    for course in range(len(listFromQuery)):                    # For each row(course info) in listFromQuery
        canReach = True                                         # Tracks if the student has all needed prerequisites
        row = listFromQuery[course]
        preReqs = list()
        if row[3] != None:
            preReqs = row[3]                                    # Index of prereqs column of course
            preReqs = parseString(preReqs)                      # Convert the string into parsed format

        if type(preReqs) != list():                             # If not the empty list
            for i in range(len(preReqs)):                       # For each item in preReqs
                if type(preReqs[i]) is list:                    # 'OR' separated prerequisites
                    if not orTrue(preReqs[i], coursesTaken):
                        canReach = False
                        break

                elif type(preReqs[i]) is tuple:                 # 'AND' separated prerequisites
                    if not andTrue(preReqs[i], coursesTaken):
                        canReach = False
                        break

                else:                                           # Single prereq
                    #courseStr = gCS.getCourseStr(preReqs[i])
                    if preReqs[i] not in coursesTaken:
                        canReach = False
                        break


        if canReach is True:                                    # If all prerequisites met add course to
            reachableCourses.append(listFromQuery[course])      # reachableCourses

    return reachableCourses                                     # Return a list of all courses whose prerequisites are
                                                                # satisfied
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query results that collide with another course taken
# 'mon' 'tues' 'wed' 'thurs' 'OnLine'. Found in column 2 of results
def pruneOffDay(listFromQuery, dayToPrune):
    dayToPrune = dayToPrune.lower()
    prunedList = []

    if dayToPrune == 'none':                                    # Does not filter any courses off of the list
        return listFromQuery

    for course in listFromQuery:
        if course[2] == 'online':                               # If courses day of week is online
            prunedList.append(course)                           # Can always include online courses

        if course[2] != dayToPrune:                             # If courses day of the week isn't dayToPrune
            prunedList.append(course)

    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query result that the student has already taken.
def pruneOffPrevCourses (listFromQuery, coursesTaken):
    prunedList = list()

    for course in listFromQuery:
        courseStr = gCS.getCourseStr(course)

        if courseStr not in coursesTaken:
            prunedList.append(course)

    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query not present in given curriculum.
def pruneByCurriculum(listFromQuery, curriculum):
    prunedList = list()

    for course in range (len(listFromQuery)):
        courseStr = gCS.getCourseStr(listFromQuery[course])

        if courseStr in curriculum.coursesInCurriculum:
            prunedList.append(listFromQuery[course])

    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Applies all filters to the original query and returns filtered list.
def filter (listFromQuery, plan, dayToPrune, curriculum):
    filter1 = pruneOffPrevCourses(listFromQuery, plan.coursesTaken)
    filter2 = pruneOffDay(filter1, dayToPrune)
    filter3 = pruneByCurriculum(filter2, curriculum)
    return pruneByPrereq(filter3, plan.coursesTaken)
