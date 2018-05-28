# JP
class Plan:
    """class that represents a curriculum at a particular point during search."""

    def __init__(self, selectionOrder, coursesTaken, termNum, maxCourses):
        self.selectionOrder = selectionOrder            # List of Lists. Inner lists represent quarters
        self.coursesTaken = coursesTaken                # Set of strings representing courses taken.  'csc300'
        self.termNum = int(termNum)                          # Number representing term in the database increments by 5s
        self.maxCourses = maxCourses                    # The maximum number of courses a student will take per quarter
        #self.currTermIdx = len(selectionOrder)          # Stores index of the current term we are preparing
        self.currTermIdx = 0  # Stores index of the current term we are preparing
        self.daysFilled = []

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

    def addCourse(self, courseInfo):
        print("adding course to plan")

        ## new code to account for the first plan which has no selectionOrder
        #if len(self.selectionOrder) == 0:
        ##if self.selectionOrder == list():
        #    print("creating initial term in selectionOrder")
        #    self.selectionOrder.append(list())
        #    print(courseInfo.getName)
        #    self.selectionOrder[0].append(courseInfo.getName)
        #    self.coursesTaken.add(courseInfo.getName)
        #    self.daysFilled.append(courseInfo.day)

        if courseInfo.getName == '' or courseInfo.getName in self.coursesTaken:
            return

        # new code to account for the first plan which has no selectionOrder
        if len(self.selectionOrder) == 0:
            # if self.selectionOrder == list():
            print("creating initial term in selectionOrder")
            self.selectionOrder.append(list())
        else:                                                       # Add a list to hold term info
            if len(self.selectionOrder) < self.currTermIdx and self.currTermIdx != 0:
                print("adding an empty term to fill")
                self.selectionOrder.append(list())


        # There is room for a class and we have been handed a class
        if len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and courseInfo.getName != '':
        #elif len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and courseInfo != []:
            print("adding course to open term")
            self.selectionOrder[self.currTermIdx].append(courseInfo.getName)
            self.coursesTaken.add(courseInfo.getName)
            print("LenCoursesTaken: " + str(len(self.coursesTaken)))
            if len(self.daysFilled) >= self.maxCourses:
                self.daysFilled = [courseInfo.day]
            else:
                self.daysFilled.append(courseInfo.day)
            print(courseInfo.getName)

        # There is room for a class but no classes are available. Advance to next term number
        elif len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and courseInfo.getName == '':
        #elif len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and courseInfo == []:
            print("adding null to term due to no results")
            self.selectionOrder[self.currTermIdx].append(courseInfo.getName)
            self.termNum = self.termNum + 5
            self.currTermIdx += 1 # recent addition
            print(courseInfo.getName)


        # There isn't any room but there are no more courses to add.
        elif len(self.selectionOrder[self.currTermIdx]) >= self.maxCourses and courseInfo.getName == '':
            print("not adding empty list, we are done")
            self.termNum = self.termNum + 5
            self.currTermIdx += 1  # recent addition
            print(courseInfo.getName)

        # There isn't any room but there are more courses to add.
        elif len(self.selectionOrder[self.currTermIdx]) >= self.maxCourses and courseInfo.getName != '':
            print("adding empty list due to no courses available in term")
            self.selectionOrder.append(list())
            self.termNum = self.termNum + 5
            self.currTermIdx += 1  # recent addition
            self.selectionOrder[self.currTermIdx].append(courseInfo.getName)
            self.coursesTaken.add(courseInfo.getName)
            print(courseInfo.getName)

        # There isn't room for another class. Advance to next term.
        else:
            print("in else")
            #print("adding empty list due to no courses available in term")
            # self.selectionOrder.append(list())
            self.termNum = self.termNum + 5
            self.currTermIdx += 1 # recent addition
            print(courseInfo.getName)
        '''
        # There is room for a class and we have been handed a class
        if len(self.selectionOrder[self.currTermIdx]) < self.maxCourses and course != list():
            print("adding course to open term")
            self.selectionOrder[self.currTermIdx].append(course.getName)
            self.coursesTaken.add(course.getName)
            self.daysFilled.append(course.daysFilled)
        '''



    # =====================================================================================================================
    # Determines which categories given course satisfies in a given curriculum.

    def classifyCourse(self, courseInfo, curriculum):
        courseType = list()

        print("classifying courses type.")
        # TODO: need to check for non-string or nothing we need to just return

        for i in range(0, len(curriculum.courseTypeDesignations)):
            if courseInfo.getName in curriculum.courseTypeDesignations[i]:
                courseType.append(i)
                print("Added " + str(i) + " to CourseType")

        return courseType

    # =====================================================================================================================

    # =====================================================================================================================
    # Indexes correspond to the number of intro, foundation, major electives, open electives, capstones, and courses
    # from a single concentration required for graduation. Credit the earliest bucket. If those are full then look at
    # the elective buckets.
    # TODO: test this
    def incrCourseType(self, courseTypes, typesTaken, gradReqs):
        print("Incrementing Course Type")
        if courseTypes == list():                                   # Course doesn't fill a courseType don't increment
            return

        for potentialFit in courseTypes:                            # For each bucket that the course fits in

            if potentialFit == 2:
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



