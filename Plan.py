import getCourseString


class Plan:
    """class that represents a curriculum at a particular point during search."""

    def __init__(self, selectionOrder, coursesTaken, termNum, maxCourses):
        self.selectionOrder = selectionOrder            # List of Lists. Inner lists represent quarters
        self.coursesTaken = coursesTaken                # # Set of strings representing courses taken.  'csc300'
        self.termNum = termNum                          # Number representing term in the database increments by 5s
        self.maxCourses = maxCourses                    # The maximum number of courses a student will take per quarter

    currTermIdx = len(selectionOrder)                   # Stores index of the current term we are preparing

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
    typesTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Adds given course to the current plans term. If no course is available, then it leaves the term partially empty
    # if something else has been added to the term. If no options are available it instead creates an empty term.
    # Once the term is full or options are exhausted it advances termNum
    def addCourse(self, course):

        # There is room for a class and we have been handed a class
        if len(self.selectionOrder[currTermIdx]) < self.maxCourses and course != list():
            courseStr = getCourseString(course)
            self.selectionOrder[currTermIdx].append(courseStr)
            self.coursesTaken.add(courseStr)

        # There is room for a class but no classes are available. Advance to next term number
        elif len(self.selectionOrder[currTermIdx]) < self.maxCourses and course == list():
            self.selectionOrder[currTermIdx].append(course)
            self.termNum = self.termNum + 5

        # There isn't room for another class. Advance to next term.
        else:
            self.selectionOrder.append(list())
            self.termNum = self.termNum + 5


