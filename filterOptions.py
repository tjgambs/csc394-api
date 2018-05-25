from getCourseStr import getCourseStr
from class_tree import class_list

# JP
# =====================================================================================================================
# Filter potential courses leaving only courses whose prerequisites are met


# Helper function for pruneByPrereq that asserts whether any element is satisfied
def orTrue (orPreReqs, coursesTaken):
    preReqs = orPreReqs

    for pre in preReqs:

        if type(pre) is list:                                   # 'OR' separated prerequisites
            if orTrue(pre, coursesTaken):                       # Something in 'OR' is present
                return True                                     # orPreReqs satisfies requirements

        elif type(pre) is tuple:                                # 'AND' separated prerequisites
            if andTrue(pre, coursesTaken):                      # Everything in 'AND' is present
                return True                                     # orPreReqs satisfies requirements

        else:
            if pre.lower() in coursesTaken:                     # Individual prereq present
                return True                                     # Report able to qualify for this course

    return False                                                # No element in 'OR' present. Unable to qualify


# Helper function for pruneByPrereq that asserts whether all elements are satisfied
def andTrue(andPreReqs, coursesTaken):
    preReqs = andPreReqs

    for pre in preReqs:                                         # For each element in preReqs

        if type(pre) is list:                                   # 'OR' separated prerequisites
            if not orTrue(pre, coursesTaken):                   # Nothing in 'OR' is present
                return False                                    # andPreReqs doesn't satisfy requirements

        elif type(pre) is tuple:                                # 'AND' separated prerequisites
            if not andTrue(pre, coursesTaken):                  # Something in 'AND' not present
                return False                                    # andPreReqs doesn't satisfy requirements

        else:
            if pre.lower() not in coursesTaken:                 # Individual prereq present
                return False                                    # Report able to qualify for this course

    return True                                                 # Every element in 'AND' present. Able to qualify


# Removes courses from the query if the student cannot qualify
def pruneByPrereq (listFromQuery, coursesTaken):
    reachableCourses = list()                                   # List of lists of course info the student qualifies for
    canReach = True                                             # Default assumption

    for courseRow in listFromQuery:                             # For each row(course info) in listFromQuery
        canReach = True                                         # Tracks if the student has all needed prerequisites
        cl = class_list()
        preReqs = cl.get_prereqs(courseRow[0].upper())          # Retrieve properly formatted preReqs from dictionary

        if preReqs == []:                                       # Course doesn't have any preReqs
            break                                               # Student qualifies for the course
        else:
            for course in preReqs:                              # For each item in preReqs
                if type(course) is list:                        # 'OR' separated prerequisites
                    if not orTrue(course, coursesTaken):
                        canReach = False
                        break

                elif type(course) is tuple:                     # 'AND' separated prerequisites
                    if not andTrue(course, coursesTaken):
                        canReach = False
                        break

                else:                                           # Single prereq
                    if course.lower() not in coursesTaken:
                        canReach = False
                        break

        if canReach is True:                                    # If all prerequisites met add course to
            reachableCourses.append(courseRow[0].lower())                     # reachableCourses

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
        if course[1] == 'OnLine':                               # If courses day of week is online      TODO: Verify that the index is where day offered is stored
            prunedList.append(course)                           # Can always include online courses

        if course[1] != dayToPrune:                             # If courses day of the week isn't dayToPrune
            prunedList.append(course)

    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query result that the student has already taken. Expects a list of rows from query
def pruneOffPrevCourses (listFromQuery, coursesTaken):
    prunedList = list()

    for courseRow in listFromQuery:
        courseStr = getCourseStr(courseRow[0])                    # TODO: See about not using getCourseStr if data allows

        if courseStr not in coursesTaken:
            prunedList.append(courseRow)

    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query not present in given curriculum. Expects a list of rows from query
def pruneByCurriculum(listFromQuery, curriculum):
    prunedList = list()

    for courseRow in listFromQuery:
        courseStr = getCourseStr(courseRow[0])                      # TODO: See about not using getCourseStr if data allows

        if courseStr in curriculum.coursesInCurriculum:
            prunedList.append(listFromQuery[courseRow])

    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Applies all filters to the original query and returns filtered list.
def filter (listFromQuery, plan, dayToPrune, curriculum):
    filter1 = pruneOffPrevCourses(listFromQuery, plan.coursesTaken)
    filter2 = pruneOffDay(filter1, dayToPrune)
    filter3 = pruneByCurriculum(filter2, curriculum)
    return pruneByPrereq(filter3, plan.coursesTaken)
