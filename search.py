from queue import PriorityQueue

# def heuristic(a, b):
# (x1, y1) = a
# (x2, y2) = b
# return abs(x1 - x2) + abs(y1 - y2)

# def aStarSearch(graph, start, goal):
# frontier = PriorityQueue()
# frontier.put(start, 0)
# cameFrom = {}
# costSoFar = {}
# cameFrom[start] = None
# costSoFar[start] = 0
#
# while not frontier.empty():
#    current = frontier.get()
#
#    if current == goal:
#        break
#
#    for next in graph.neighbors(current):
#        newCost = costSoFar[current] + graph.cost(current, next)
#        if next not in costSoFar or new_cost < costSoFar[next]:
#            costSoFar[next] = new_cost
#            priority = new_cost + heuristic(goal, next)
#            frontier.put(next, priority)
#            cameFrom[next] = current
#
# return cameFrom, costSoFar



def heuristics(course):
    rarity = course.getH1                   # Update this once you know how the scores are stored in database
    unlocks = course.getH2
    return rarity + unlocks


def isGoal(plan, curriculum):
    if curriculum.introductory_courses      <= plan.coursesTaken[0] \
        and curriculum.foundation_courses   <= plan.coursesTaken[1] \
        and curriculum.gradReqs[2]          <= plan.typesTaken[2] \
        and curriculum.gradReqs[3]          <= plan.typesTaken[3]:

        for i in range(4, len(plan.typesTaken)):
            if curriculum.gradReqs[4]       <= plan.typesTaken[i]:
                return True
    else:
        return False


def generateCoursePlan(start, goal, maxCourses):
    'Takes a starting plan, an end goal or Curriculum, and the max number of classes per quarter and generates the shortest path to graduation'
    # Start should be a Plan() and will include any classes the student has already taken to this point. It should have accurate counts of its course typesTaken before starting the search.
    # Goal is the end state desired by the user. Usually this will be a Curriculum object which will allow gradReqs to be determined, but this could also be used to create limited searches.
    # MaxCourses is the max number of courses a student is willing to take in a given quarter.

    # Cost should represent how many quarters are needed to graduate. They should however be multiplied by some factor so that they are larger than our heuristic values. Our heuristics
    # should produce values for rarity that are 16 - # of times offered in 16 quarters. So the values will range between 0-16. Unlocks could be anything between 0 and the # of total classes.
    # My expectation is that a class will have less than 16 unlocks. If this is not the case then the cost formula needs to be revised. We never want to over-estimate the cost of a path to
    # graduation.
    # 32 is chosen because it is a guess of the maximum value of h(n). This value should equal max(rarity) + max(unlocks)
    # g(n) = (quarters x 32) or cost so far
    # h(n) = 32 - (rarity + unlocks)
    # f(n) = g(n) + h(n)
    # Record actual cost of a path as g(n) / 32 = number of quarters to graduate.
    # A course that is offered every quarter and unlocks nothing will cost 32 which is exactly what adding a class costs. Selecting something more rare, and/or unlocks more classes will appear
    # to cost less than a normal quarter. So the path will be an under-estimate of cost and therefore it will be admissible. As long as unlocks is less than 16 we will never have negative costs
    # therefore h(n) will be considered consistent.

    frontier = PriorityQueue()
    frontier.put(start, 0)
    cameFrom = {}
    costSoFar = {}
    cameFrom[start] = None
    costSoFar[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if isGoal(current, goal):
            break

        for suggestedCourse in getOptions():
            new_cost = costSoFar[current] + 32                      # 32 is the arbitrary constant cost of selecting a class described above
            suggestedPlan = Plan(current.selectionOrder, current.coursesTaken, current.termNum)
            suggestedPlan.addCourse(suggestedCourse)

            if suggestedPlan not in costSoFar or new_cost < costSoFar[suggestedPlan]:
                costSoFar[suggestedPlan] = new_cost
                priority = new_cost + heuristics(suggestedCourse)
                frontier.put(suggestedPlan, priority)