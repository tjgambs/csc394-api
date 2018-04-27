class Plan:
    'class that represents a curriculum at a particular point during search'

    def __init__(self, selectionOrder, coursesTaken, termNum):
        self.selectionOrder = selectionOrder
        self.coursesTaken = coursesTaken
        self.termNum = termNum

    selectionOrder = []
    coursesTaken = set()
    termNum = 0

    # Count of each type of course taken at this point in the plan. Used for goal checking.
    # Each index represents a type of course. Stores the int num of that type taken
    typesTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    # Indexes correspond to the following course types
    # 0:  Introductory Courses
    # 1:  Foundation Courses
    # 2:  Major Elective Courses
    # 3:  Open Elective Courses
    # 4:  Software Systems Development Courses
    # 5:  Theory Courses = 0
    # 6:  Data Science Courses
    # 7:  Database Systems Courses
    # 8:  AI Courses
    # 9:  Software Engineering Courses
    # 10: Game and Real-Time Systems Courses
    # 11: Human-Computer Interaction Courses