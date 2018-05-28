from Queue import PriorityQueue
from app.logic.Plan import Plan
from app.logic.Curriculum import Curriculum
from app.models.term_courses import TermCourses
from app.logic.filterOptions import filter

# JP
# =====================================================================================================================
def heuristics(course, suggestedPlan, user):
    """ Assigns a score to the coursePlan based on the rarity of the course, the number of courses this one makes
    available in the future, and the users need and preference for a particular type of elective"""

    score = course.score
    bonus = 0

    ''' currently our users store this differently than im expecting check that 
    if suggestedPlan.typesTaken[2] < user.curriculum.gradReqs[2]:            # If user needs more electives
        #userPref = user.elective
        if course.getName in user.curriculum.courseTypeDesignations[user.elective]:  # Add bonus if course is preferred
            bonus += 5

        # If the course is a member of the users most frequently taken elective course type and the user has not
        # met the minimum number of courses from a single concentration requirement, add a weight
        electivesCount = ()
        for i in range(5, 13):
            electivesCount.append(suggestedPlan.typesTaken[i])
        if max(electivesCount) < user.curriculum.gradReqs[5]:
            if course in user.curriculum.courseTypeDesignation[electivesCount.index(max())]:
                bonus += 5
    '''
    print("returning heuristic score: " + str(score + bonus))
    return score + bonus
    #return rarity + unlocks + bonus
# =====================================================================================================================


# =====================================================================================================================
# Determines if the current plan is a goal state
def isGoal(plan, curriculum):
    if curriculum.introductory_courses      <= plan.coursesTaken \
        and curriculum.foundation_courses   <= plan.coursesTaken \
        and curriculum.gradReqs[2]          <= plan.typesTaken[2] \
        and curriculum.gradReqs[3]          <= plan.typesTaken[3] \
        and curriculum.gradReqs[4]          <= plan.typesTaken[4] \
        and curriculum.gradReqs[6]          <= plan.typesTaken[13]:

        for i in range(5, len(plan.typesTaken)):
            if curriculum.gradReqs[5]       <= plan.typesTaken[i]:
                return True
    else:
        return False
# =====================================================================================================================
# Adds the given suggested course into the suggested plan. Then it updates the typesTaken lists inside of the Plan.
def addUpdateCourse(suggestedPlan, suggestedCourseInfo, curriculum):
    if suggestedCourseInfo.getName not in suggestedPlan.coursesTaken:
        suggestedPlan.addCourse(suggestedCourseInfo)
        courseTypeList = suggestedPlan.classifyCourse(suggestedCourseInfo, curriculum)
        suggestedPlan.incrCourseType(courseTypeList, suggestedPlan.typesTaken, curriculum.gradReqs)

# =====================================================================================================================
def automated(user):
    """Takes a user object and generates the shortest path to graduation. """

    # Start should be a Plan() and will include any classes the user has already taken to this point. It should have
    # accurate counts of its course typesTaken before starting the search. Goal is the end state desired by the user.
    # Usually this will be the gradReqs for the users Curriculum object, but this could also be used to create
    # limited searches. number_of_classes_per_quarter is the max number of courses a user is willing to take in a
    # given quarter.

    # Cost should represent how many quarters are needed to graduate. They should however be multiplied by some factor
    # so that they are larger than our heuristic values. Our heuristics should produce values for rarity that are 8 - #
    # of times offered in 8 quarters. So the values will range between 0-8. Unlocks could be anything between 0 and
    # the # of total classes opened up by taking it. My expectation is that a class will have less than 16 unlocks. If
    # this is not the case then the cost formula needs to be revised. We never want to over-estimate the cost of a path
    # to graduation. 100 is chosen because it is the maximum value of h(n) seen in our data.
    # Should equal max(rarity) + max(unlocks) + bonus
    # g(n) = (quarters x 100) or cost so far
    # h(n) = 100 - (rarity + unlocks + bonus)
    # f(n) = g(n) + h(n)
    # Record actual cost of a path as g(n) / 100 = number of quarters to graduate.
    # A course that is offered every quarter and unlocks nothing and does not match a preferred elective type will cost
    # 100 which is exactly what adding a class costs. Selecting something more rare, and/or unlocks more classes will
    # appear to cost less than a normal quarter. So the path will be an under-estimate of cost and therefore it will be
    # admissible. As long as unlocks is less than 16 we will never have negative costs therefore h(n) will be considered
    # consistent  .

    print("entering the while loop")
    start = Plan(list(), user.getCoursesTaken, user.getTerm, user.compMaxCourses)
    curriculum = user.curriculum
    frontier = PriorityQueue()
    frontier.put(start, 0)
    cameFrom = {}
    costSoFar = {}
    cameFrom[start] = None
    costSoFar[start] = 0
    stdCost = 100                # TODO: The arbitrary constant cost of selecting a class described above

    while not frontier.empty():
        print("Frontier Size: " + str(frontier.qsize()))
        current = frontier.get()
        print("pop off frontier")

        if isGoal(current, curriculum):
            print("goal check true")
            break
        print("not in goal state")

        print("TermNum: " + str(current.termNum))
        queryResults = TermCourses.getOptions(current.termNum)
        print(len(queryResults))
        print("query")
        #break # delete me
        filteredResults = filter(queryResults, current, current.daysFilled, curriculum)
        print("query resulted in: " + str(len(filteredResults)))

        # Restricting the filteredResults to a managable size. Limiting it to best 4
        if len(filteredResults) > 4:
            maxResults = 4
        else:
            maxResults = len(filteredResults)
        restrictedResults = []
        for i in range(0, maxResults):
            restrictedResults.append(filteredResults[i])

        #for suggestedCourseInfo in filteredResults:
        for suggestedCourseInfo in restrictedResults:
            print("SuggestedCourseInfo ========================")

            suggestedCourse = suggestedCourseInfo.getName
            print(suggestedCourse)
            new_cost = costSoFar[current] + stdCost
            suggestedPlan = Plan(current.selectionOrder, current.coursesTaken, current.termNum, user.compMaxCourses)
            print("creating new plan")
            addUpdateCourse(suggestedPlan, suggestedCourseInfo, curriculum) #changed from suggestedCourse to suggestedCourseInfo
            print("updating plan to include course")

            if suggestedPlan not in costSoFar or new_cost < costSoFar[suggestedPlan]:
                print("update plan cost")
                costSoFar[suggestedPlan] = new_cost
                priority = new_cost + (stdCost - heuristics(suggestedCourseInfo, suggestedPlan, user))
                frontier.put(suggestedPlan, priority)
                print("add suggestedPlan to frontier")
                cameFrom[suggestedPlan] = current
                print("update cameFrom")
                print("============================================")

    print(current.selectionOrder)
    return current.selectionOrder
# =====================================================================================================================
