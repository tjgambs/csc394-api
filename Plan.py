import getCourseStr as gCS


# JP
class Plan:
    """class that represents a curriculum at a particular point during search."""

    def __init__(self, selectionOrder, coursesTaken, termNum, maxCourses):
        self.selectionOrder = selectionOrder            # List of Lists. Inner lists represent quarters
        self.coursesTaken = coursesTaken                # Set of strings representing courses taken.  'csc300'
        self.termNum = termNum                          # Number representing term in the database increments by 5s
        self.maxCourses = maxCourses                    # The maximum number of courses a student will take per quarter
        self.currTermIdx = len(selectionOrder)          # Stores index of the current term we are preparing

        # Count of each type of course taken at this point in the plan. Used for goal checking.
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

        self.typesTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Adds given course to the current plans term. If no course is available, then it leaves the term partially empty
    # if something else has been added to the term. If no options are available it instead creates an empty term.
    # Once the term is full or options are exhausted it advances termNum
    def addCourse(self, course):

        # There is room for a class and we have been handed a class
        if len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and course != list():
            courseStr = gCS.getCourseStr(course)
            self.selectionOrder[self.currTermIdx].append(courseStr)
            self.coursesTaken.add(courseStr)

        # There is room for a class but no classes are available. Advance to next term number
        elif len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and course == list():
            self.selectionOrder[self.currTermIdx].append(course)
            self.termNum = self.termNum + 5

        # There isn't room for another class. Advance to next term.
        else:
            self.selectionOrder.append(list())
            self.termNum = self.termNum + 5

    # =====================================================================================================================
    # Determines which categories given course satisfies in a given curriculum.
    def classifyCourse(course, curriculum):
        courseStr = gCS.getCourseStr(course)
        courseType = list()

        # TODO: need to check for non-string or nothing we need to just return

        for i in range(0, len(curriculum.courseTypeDesignations)):
            if courseStr in curriculum.courseTypeDesignations[i]:
                courseType.append(i)

        return courseType

    # =====================================================================================================================

    # =====================================================================================================================
    # Indexes correspond to the number of intro, foundation, major electives, open electives, capstones, and courses \
    # from a single concentration required for graduation
    # Credit the earliest bucket. If those are full then look at the elective buckets.
    def incrCourseType(courseTypes, typesTaken, gradReqs):
        for i in range(len(courseTypes)):                           # courseTypes (list) of all buckets the course fills
            if courseTypes[i] < 5:                                  # Course = Intro, Foundation, Major E, or Open E
                if typesTaken[courseTypes[i]] < gradReqs[i]:        # If the bucket that matches class type isn't full
                    typesTaken[i] = typesTaken[i] + 1               # Increment that bucket
                    return
            elif courseTypes[i] == 13:                              # courseType is an Advanced Course
                if typesTaken[courseTypes[i]] < gradReqs[13]:       # If the advanced course bucket isn't full
                    typesTaken[i] = typesTaken[i] + 1               # Increment advanced course bucket count
                    return
            elif (courseTypes[i] < 13) and (courseTypes[i] >= 5):   # courseType is a CS focus bucket
                typesTaken[i] = typesTaken[i] + 1                   # Increment specific focus bucket
                typesTaken[5] = typesTaken[5] + 1                   # Increment max courses in specific bucket
                return
            else:                                                   # Course didn't match
                return

    # =====================================================================================================================



