# JP


class Plan:
    """class that represents a curriculum at a particular point during search."""

    def __init__(self, selectionOrder, coursesTaken, termNum, maxCourses, currTermIdx, typesTaken):
        self.selectionOrder = selectionOrder            # List of Lists. Inner lists represent quarters
        self.coursesTaken = coursesTaken                # Set of strings representing courses taken.  'csc300'
        self.termNum = int(termNum)                     # Number representing term in the database increments by 5s
        self.maxCourses = maxCourses                    # The maximum number of courses a student will take per quarter
        self.currTermIdx = currTermIdx                  # Stores index of the current term we are preparing
        self.daysFilled = []                            # Days filled with courses in current term
        self.typesTaken = typesTaken
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
        

    @property
    def term_finished(self):
        return len(self.selectionOrder[self.currTermIdx]) == self.maxCourses

    @property
    def _id(self):
        return ''.join([y for x in self.selectionOrder for y in x])

    # Adds given course to the current plans term. If no course is available, then it leaves the term partially empty
    # if something else has been added to the term. If no options are available it instead creates an empty term.
    # Once the term is full or options are exhausted it advances termNum

    def addCourse(self, courseInfo):

        # new code to account for the first plan which has no selectionOrder
        if len(self.selectionOrder) == self.currTermIdx:
            self.selectionOrder.append([courseInfo.getName])
            self.coursesTaken.add(courseInfo.getName)
            if len(self.daysFilled) >= self.maxCourses:                 # Clears the daysFilled when we change terms
                self.daysFilled = [courseInfo.day]
            else:
                self.daysFilled.append(courseInfo.day)

        # There is room for a class and we have been handed a class
        elif len(self.selectionOrder[self.currTermIdx]) < self.maxCourses:
            self.selectionOrder[self.currTermIdx].append(courseInfo.getName)
            self.coursesTaken.add(courseInfo.getName)
            if len(self.daysFilled) >= self.maxCourses:                 # Clears the daysFilled when we change terms
                self.daysFilled = [courseInfo.day]
            else:
                self.daysFilled.append(courseInfo.day)

        if len(self.selectionOrder[self.currTermIdx]) == self.maxCourses:
            self.selectionOrder.append([])
            self.termNum = self.termNum + 5
            self.currTermIdx += 1



    # =====================================================================================================================
    # Determines which categories given course satisfies in a given curriculum.

    def classifyCourse(self, courseInfo, curriculum):
        courseType = list()
        for i in range(0, len(curriculum.courseTypeDesignations)):
            if courseInfo.getName in curriculum.courseTypeDesignations[i]:
                courseType.append(i)
        return courseType

    # =====================================================================================================================

    # =====================================================================================================================
    # Indexes correspond to the number of intro, foundation, major electives, open electives, capstones, and courses
    # from a single concentration required for graduation. Credit the earliest bucket. If those are full then look at
    # the elective buckets.
    # TODO: test this
    def incrCourseType(self, courseTypes, typesTaken, gradReqs):
        if courseTypes == list():                                   # Course doesn't fill a courseType don't increment
            return

        for potentialFit in courseTypes:                            # For each bucket that the course fits in

            if potentialFit == 2:                                   # This allows credit for both major e and focus
                typesTaken[2] += 1

            if potentialFit < 5:                                    # Course = Intro, Foundation, Major E, or Open E
                for i in range(0, 5):                               # Loop through buckets

                    if typesTaken[i] < gradReqs[i] \
                            and potentialFit == i \
                            and potentialFit != 2:                  # If the bucket that matches class type isn't full
                        typesTaken[i] += 1                          # Increment that bucket
                        return

            elif potentialFit == 13:                                # Course is an Advanced Course
                if typesTaken[13] < gradReqs[6]:                    # If the advanced course bucket isn't full
                    typesTaken[13] += 1                             # Increment advanced course bucket count
                    return

            elif (potentialFit < 13) and (potentialFit >= 5):       # Course fits at least one CS focus area
                for i in range(5, 13):                              # Loop through focus area buckets
                    if typesTaken[i] < gradReqs[5]\
                            and potentialFit == i:                 # If the bucket that matches class type isn't full
                        typesTaken[i] += 1                          # Increment specific focus bucket
                        return

            else:                                                   # Course didn't match
                return
    # =====================================================================================================================



