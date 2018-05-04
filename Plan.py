class Plan:
    'class that represents a curriculum at a particular point during search'

    def __init__(self, selectionOrder, coursesTaken, termNum, maxCourses):
        self.selectionOrder = selectionOrder
        self.coursesTaken = coursesTaken
        self.termNum = termNum
        self.maxCourses = maxCourses

    selectionOrder = []
    coursesTaken = set()
    termNum = 0

    # Count of each type of course taken at this point in the plan. Used for goal checking.
    # Each index represents a type of course. Stores the int num of that type taken
    typesTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def addCourse(self, course):
        if len(self.selectionOrder[self.termNum]) < self.maxCourses:
            self.selectionOrder[self.termNum].append(course)
        else:
            self.selectionOrder.append(list(course))
            self.termNum = self.termNum + 1             # modify it to match how the database handles it

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
    # 10:  Software Engineering Courses
    # 11: Game and Real-Time Systems Courses
    # 12: Human-Computer Interaction Courses
