from queue import PriorityQueue
import Plan
import Student
import GetOptions


def heuristics(course, suggestedPlan, student):
    """ Assigns a score to the coursePlan based on the rarity of the course, the number of courses this one makes
    available in the future, and the students need and preference for a particular type of elective"""

    rarity = course.getH1                   # TODO: Update this once you know how the scores are stored in database
    unlocks = course.getH2
    bonus = 0

    if suggestedPlan.typesTaken[2] < student.curriculum.gradReqs[2]:           # If the student needs more electives
        studentPref = student.elective_preference
        if course in student.curriculum.courseTypeDesignation[studentPref]:    # Add bonus if course is preferred
            bonus += 5

        # If the course is a member of the students most frequently taken elective course type and the student has not
        # met the minimum number of courses from a single concentration requirement, add a weight
        electivesCount = ()
        for i in range(5, 13):
            electivesCount.append(suggestedPlan.typesTaken[i])
        if max(electivesCount) < student.curriculum.gradReqs[5]:
            if course in student.curriculum.courseTypeDesignation[electivesCount.index(max())]:
                bonus += 5
    return rarity + unlocks + bonus


def isGoal(plan, curriculum):
    if curriculum.introductory_courses      <= plan.coursesTaken \
        and curriculum.foundation_courses   <= plan.coursesTaken \
        and curriculum.gradReqs[2]          <= plan.typesTaken[2] \
        and curriculum.gradReqs[3]          <= plan.typesTaken[3] \
        and curriculum.gradReqs[4]          <= plan.typesTaken[4]:

        for i in range(5, len(plan.typesTaken)):
            if curriculum.gradReqs[5]       <= plan.typesTaken[i]:
                return True
    else:
        return False


def classifyCourse (course, curriculum):
    for typ


def automated(student):
    """Takes a student object and generates the shortest path to graduation. """

    # Start should be a Plan() and will include any classes the student has already taken to this point. It should have
    # accurate counts of its course typesTaken before starting the search. Goal is the end state desired by the user.
    # Usually this will be the gradReqs for the students Curriculum object, but this could also be used to create
    # limited searches. number_of_classes_per_quarter is the max number of courses a student is willing to take in a
    # given quarter.

    # Cost should represent how many quarters are needed to graduate. They should however be multiplied by some factor
    # so that they are larger than our heuristic values. Our heuristics should produce values for rarity that are 16 - #
    # of times offered in 16 quarters. So the values will range between 0-16. Unlocks could be anything between 0 and
    # the # of total classes. My expectation is that a class will have less than 16 unlocks. If this is not the case
    # then the cost formula needs to be revised. We never want to over-estimate the cost of a path to graduation.
    # 42 is chosen because it is a guess of the maximum value of h(n). Should equal max(rarity) + max(unlocks) + bonus
    # g(n) = (quarters x 42) or cost so far
    # h(n) = 42 - (rarity + unlocks + bonus)
    # f(n) = g(n) + h(n)
    # Record actual cost of a path as g(n) / 42 = number of quarters to graduate.
    # A course that is offered every quarter and unlocks nothing and does not match a preferred elective type will cost
    # 42 which is exactly what adding a class costs. Selecting something more rare, and/or unlocks more classes will
    # appear to cost less than a normal quarter. So the path will be an under-estimate of cost and therefore it will be
    # admissible. As long as unlocks is less than 16 we will never have negative costs therefore h(n) will be considered
    # consistent.

    maxCourses = student.number_of_classes_per_quarter
    start = Plan(list(), student.courses_taken, student.current_quarter, maxCourses)
    curriculum = student.curriculum
    frontier = PriorityQueue()
    frontier.put(start, 0)
    cameFrom = {}
    costSoFar = {}
    cameFrom[start] = None
    costSoFar[start] = 0
    stdCost = 42                # TODO: The arbitrary constant cost of selecting a class described above

    while not frontier.empty():
        current = frontier.get()

        if isGoal(current, curriculum):
            break

        for suggestedCourse in GetOptions(student.curriculum, current):   # TODO: getOptions will be the database query

            new_cost = costSoFar[current] + stdCost
            suggestedPlan = Plan(current.selectionOrder, current.coursesTaken, current.termNum, maxCourses)
            suggestedPlan.addCourse(suggestedCourse)
            # TODO: Update coursesTaken to account for added course

            if suggestedPlan not in costSoFar or new_cost < costSoFar[suggestedPlan]:
                costSoFar[suggestedPlan] = new_cost
                priority = new_cost + (stdCost - heuristics(suggestedCourse, suggestedPlan, student))
                frontier.put(suggestedPlan, priority)
                cameFrom[suggestedPlan] = current

    return current.selectionOrder