from app.logic.class_tree import class_list

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
        #print("getting class_list for prereqs")
        cl = class_list()
        #print("getting prereqs in proper format")
        preReqs = cl.class_tree.get(courseRow.getName.upper())or []
        #preReqs = cl.get_prereqs(courseRow.getName.upper())    # Retrieve properly formatted preReqs from dictionary

        for course in preReqs:  # For each item in preReqs
            # #print("Looping through prereqs")
            if type(course) is list:  # 'OR' separated prerequisites
                # print("found an OR")
                if not orTrue(course, coursesTaken):
                    # print("OR condition not met")
                    canReach = False
                    break

            elif type(course) is tuple:  # 'AND' separated prerequisites
                # print("found an AND")
                if not andTrue(course, coursesTaken):
                    # print("AND condition not met")
                    canReach = False
                    break

            else:  # Single prereq
                # print("found a string")
                if course.lower() not in coursesTaken:
                    # print("String condition not met")
                    canReach = False
                    break
        '''
        if preReqs == []:                                       # Course doesn't have any preReqs
            continue
        else:
            for course in preReqs:                              # For each item in preReqs
                # #print("Looping through prereqs")
                if type(course) is list:                        # 'OR' separated prerequisites
                    # print("found an OR")
                    if not orTrue(course, coursesTaken):
                        #print("OR condition not met")
                        canReach = False
                        break

                elif type(course) is tuple:                     # 'AND' separated prerequisites
                    #print("found an AND")
                    if not andTrue(course, coursesTaken):
                        #print("AND condition not met")
                        canReach = False
                        break

                else:                                           # Single prereq
                    #print("found a string")
                    if course.lower() not in coursesTaken:
                        #print("String condition not met")
                        canReach = False
                        break
            '''

        if canReach is True:                                    # If all prerequisites met add course to
            #print("appending course we have prereqs for")
            reachableCourses.append(courseRow)                  # reachableCourses
    print("returning reachableCourses from preReq Filter: " + str(len(reachableCourses)))
    return reachableCourses                                     # Return a list of all courses whose prerequisites are
                                                                # satisfied
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query results that collide with another course taken
# 'mon' 'tues' 'wed' 'thurs' 'OnLine'. Found in column 2 of results
def pruneOffDay(listFromQuery, daysToPrune):
    if daysToPrune == []:
        return listFromQuery
    prunedList = []
    for day in daysToPrune:
        day = day.lower()
        for course in listFromQuery:
            if course.day == 'OnLine':                           # If courses day of week is online      TODO: Verify that the index is where day offered is stored
                prunedList.append(course)                        # Can always include online courses
            elif course.day != day:                             # If courses day of the week isn't dayToPrune
                prunedList.append(course)
    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query result that the student has already taken. Expects a list of rows from query
def pruneOffPrevCourses (listFromQuery, coursesTaken):
    prunedList = list()
    for courseRow in listFromQuery:
        if courseRow.getName.lower() not in coursesTaken:
            prunedList.append(courseRow)
    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Removes courses from the query not present in given curriculum. Expects a list of rows from query
def pruneByCurriculum(listFromQuery, curriculum):
    prunedList = list()
    for courseRow in listFromQuery:
        if courseRow.getName.lower() in curriculum.coursesInCurriculum:
            prunedList.append(courseRow)
    return prunedList
# =====================================================================================================================

# =====================================================================================================================
# Applies all filters to the original query and returns filtered list.
def filter (listFromQuery, plan, dayToPrune, curriculum):
    print("Length of listFromQuery at start of filter: " + str(len(listFromQuery)))
    filter1 = pruneOffPrevCourses(listFromQuery, plan.coursesTaken)
    print("Length of filter1 after prevCourses: " + str(len(filter1)))
    filter2 = pruneOffDay(filter1, dayToPrune)
    print("Length of filter2 after pruneDay: " + str(len(filter2)))
    filter3 = pruneByCurriculum(filter2, curriculum)
    print("Length of filter3 after curriculum: " + str(len(filter3)))
    return pruneByPrereq(filter3, plan.coursesTaken)
