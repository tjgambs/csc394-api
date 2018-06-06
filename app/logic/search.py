from Queue import PriorityQueue
from app.models.plan import Plan
from app.models.term_courses import TermCourses
from app.logic.filterOptions import *
from operator import itemgetter, attrgetter
from app.models.curriculums import *
import copy

# JP
# ======================================================================================================================
def heuristics(course, suggestedPlan, user):
    """ Assigns a score to the coursePlan based on the rarity of the course, the number of courses this one makes
    available in the future, and the users need and preference for a particular type of elective"""
    score = course.score
    bonus = 0
    return score + bonus
# ======================================================================================================================


# ======================================================================================================================
# Determines if the current_plan plan is a goal state
# gradReq[2]: Major Elect, gradReq[3]: Open Elect, gradReq[4]: Capstone, gradReq[5]: Num courses req in same focus
def isGoal(plan, curriculum, courseLimit, userPref):
    types = plan.typesTaken
    if curriculum.introductory_courses      <= plan.coursesTaken \
        and curriculum.foundation_courses   <= plan.coursesTaken \
        and curriculum.gradReqs[2]          <= plan.typesTaken[2] \
        and curriculum.gradReqs[3]          <= plan.typesTaken[3] \
        and curriculum.gradReqs[4]          <= plan.typesTaken[4] \
        and curriculum.gradReqs[6]          <= plan.typesTaken[13]\
        and types[0] + types[1] + types[2]  <  courseLimit:                           # Max classes in a plan

        # If plan includes the number of courses in preferred bucket to graduate return True
        if curriculum.gradReqs[5] <= plan.typesTaken[userPref]:
            return True
    else:
        return False
# ======================================================================================================================


# ======================================================================================================================
# Adds the given suggested course into the suggested plan. Then it updates the typesTaken lists inside of the Plan.
def addUpdateCourse(suggestedPlan, suggestedCourseInfo, curriculum):
    if suggestedCourseInfo.getName not in suggestedPlan.coursesTaken:                 # Ensure no duplication of courses
        suggestedPlan.addCourse(suggestedCourseInfo)
        courseTypeList = suggestedPlan.classifyCourse(suggestedCourseInfo, curriculum)
        suggestedPlan.incrCourseType(courseTypeList, suggestedPlan.typesTaken, curriculum.gradReqs)
# ======================================================================================================================


# ======================================================================================================================
# Adds a bonus to various course types to emphasize them. Then it resorts the courses by the adjusted scores.
def modifyHeuristics(userPref, queryResults, terms, curriculum):
    if curriculum is CS:
        # Adding weights to increase importance of intro, foundation, and users focus.
        for term in terms:
            for row in queryResults[term]:
                # Add a bonus to Intro Courses
                if row.getName in curriculum.courseTypeDesignations[0]:
                    row.score += 35
                # Add a bonus to Foundation Courses
                if row.getName in curriculum.courseTypeDesignations[1]:
                    row.score += 40
                # Add a bonus to Major Elective Focus Courses
                if row.getName in curriculum.courseTypeDesignations[userPref]:
                    row.score += 20
                # Add an additional bonus to Major Elective Focus Courses if curriculum is CSC with Theory focus
                if userPref == 6:
                    if row.getName in curriculum.courseTypeDesignations[6]:
                        row.score += 30
                    if row.getName in curriculum.courseTypeDesignations[6]:
                        row.score += 50
            queryResults[term] = sorted(queryResults[term], key=attrgetter('score'), reverse=True)
        return queryResults
    else:
        # Adding weights to increase importance of intro, foundation, advanced courses, and capstone.
        for term in terms:
            for row in queryResults[term]:
                # Add a bonus to Intro Courses
                if row.getName in curriculum.courseTypeDesignations[0]:
                    row.score += 50
                # Add a bonus to Foundation Courses
                if row.getName in curriculum.courseTypeDesignations[1]:
                    row.score += 25
                # Add a bonus to Major Elective Courses if the curriculum is IS_DBA
                if curriculum == IS_DBA :
                    if row.getName in curriculum.courseTypeDesignations[2]:
                        row.score += 10
                # Add a bonus to Capstone Courses
                if row.getName in curriculum.courseTypeDesignations[4]:
                    row.score += 27
                # Add a bonus to Advanced Courses
                if row.getName in curriculum.courseTypeDesignations[13]:
                    row.score += 50
                # Add a bonus to Advanced Courses if the curriculum is IS_BI
                if curriculum == IS_BI:
                    if row.getName in curriculum.courseTypeDesignations[13]:
                        row.score += 20
            queryResults[term] = sorted(queryResults[term], key=attrgetter('score'), reverse=True)
        return queryResults
# ======================================================================================================================


# ======================================================================================================================
# Returns a standard cost for selecting courses based on curriculum type. Allows room for heuristic adjustments
def setStdCost(curriculum):
    if curriculum is CS:
        return 85
    else:
        return 100
# ======================================================================================================================


# ======================================================================================================================
# If the student had an undergraduate degree type that matches their masters degree we can credit them for the intros
def waiveCourses(startingPlan, undergrad, curriculum):
    if undergrad == 'Computer Science' and curriculum is CS:
        startingPlan.typesTaken[0] = 6
        for course in curriculum.introductory_courses:
            startingPlan.coursesTaken.add(course)
        return startingPlan

    elif undergrad == 'Information Science' and curriculum is IS_BI:
        startingPlan.typesTaken[0] = 2
        for course in curriculum.introductory_courses:
            startingPlan.coursesTaken.add(course)
        return startingPlan

    elif undergrad == 'Information Science' and curriculum is IS_DBA:
        startingPlan.typesTaken[0] = 1
        for course in curriculum.introductory_courses:
            startingPlan.coursesTaken.add(course)
        return startingPlan

    else:
        return startingPlan


# ======================================================================================================================


# ======================================================================================================================
# Prevents the search from running too long and taking up too much memory.
def timedOut(plansPopped):
    if plansPopped >= 18000:
        return True
    else:
        return False

# ======================================================================================================================


# ======================================================================================================================
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
    # the # of total classes opened up by taking it. Unlocks seems to range between 0-281. We opted to cap this number
    # to 50. We decided to cap the unlocks score to 50 and in order to have rarity weigh as much as unlocks we opted to
    # multiply its results by 6. The result is that rarity ranges between 0-42 and unlocks ranges from 0-50. We never
    # want to over-estimate the cost of a path to graduation. 50 is chosen because it is the maximum value of h(n) seen
    # in our data.
    # Should equal max(rarity) + max(unlocks) + bonus
    # g(n) = (quarters x stdCost) or cost so far
    # h(n) = stdCost - (rarity + unlocks + bonus)
    # f(n) = g(n) + h(n)
    # Record actual cost of a path as g(n) / stdCost = number of quarters to graduate.
    # A course that is offered every quarter and unlocks nothing and does not match a preferred elective type will cost
    # stdCost which is exactly what adding a class costs. Selecting something more rare, and/or unlocks more classes
    # will appear to cost less than a normal quarter. So the path will be an under-estimate of cost and therefore it
    # will be admissible. As long as stdCost is >= h(n) we will never have negative costs therefore h(n) will be
    # considered consistent.
    # stdCost must = max(rarity) + max(unlocks) + max(bonus)

    # Should we disallow online courses?
    removeOnline = user.disallowOnline

    # Get students undergrad degree type
    undergrad = user.undergraduate_degree

    # Setup Curriculum
    curriculum = user.curriculum

    # Setup concentration
    if curriculum is CS:
        userPref = int(user.getCSFocus)
    else:
        userPref = 1


    # Create null node
    start = Plan(
        selectionOrder = list(),
        coursesTaken = user.getCoursesTaken,
        termNum = user.getTerm,
        currTermIdx = 0,
        daysFilled = [],
        maxCourses = user.max_courses,
        typesTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        selectionsWithDay = list()
    )

    # If the users undergrad type matches their graduate type waive introductory courses
    start = waiveCourses(start, undergrad, curriculum)

    # Initialize variables
    frontier = PriorityQueue()
    frontier.put(start, 0)
    costSoFar = {}
    stdCost = setStdCost(curriculum)
    courseLimit = 20                                                              # max number of courses in a solution

    # Store results of the query once for reuse later in search
    terms = ['0975', '0980', '0985', '0990', '0995', '1000', '1005']
    queryResults = dict((term, TermCourses.getAvailableCourses(term)) for term in terms)

    # Modify the heuristic score of classes to emphasize certain course types and the students focus in particular
    queryResults = modifyHeuristics(userPref, queryResults, terms, curriculum)

    plansPopped = 0
    while not frontier.empty():
        # Select current plan
        curr_plan = frontier.get()
        plansPopped += 1

        # If the search has gone on too long return an empty list so the user can restart the search
        if timedOut(plansPopped):
            return list()

        # Goal Checking
        if isGoal(curr_plan, curriculum, courseLimit, userPref):
            break

        # Count up non-capstone courses in plan
        cur = curr_plan.typesTaken
        tot = cur[0] + cur[1] + cur[2] + cur[13]

        # Filter the query removing courses that the student cannot take
        subsetResults = queryResults[TermCourses.convert_stream(curr_plan.termNum)]
        filteredResults = filter(subsetResults, curr_plan, curr_plan.daysFilled, curriculum, tot, removeOnline)

        # Loop through the top 8 filtered results and try each suggested plan
        for suggestedCourseInfo in filteredResults[:8]:
            suggestedPlan = Plan(
                selectionOrder      = copy.deepcopy(curr_plan.selectionOrder),
                coursesTaken        = copy.deepcopy(curr_plan.coursesTaken),
                termNum             = copy.deepcopy(curr_plan.termNum),
                currTermIdx         = copy.deepcopy(curr_plan.currTermIdx),
                daysFilled          = copy.deepcopy(curr_plan.daysFilled),
                maxCourses          = user.max_courses,
                typesTaken          = copy.deepcopy(curr_plan.typesTaken),
                selectionsWithDay   = copy.deepcopy(curr_plan.selectionsWithDay))

            # Add suggested course to current plan
            addUpdateCourse(suggestedPlan, suggestedCourseInfo, curriculum)

            # Calculate the true cost of the current plan (non heuristic)
            new_cost = costSoFar.get(str(curr_plan.coursesTaken), costSoFar.get(str(curr_plan.coursesTaken), 0))+stdCost

            # Do not explore plans with excessive numbers of courses
            taken = suggestedPlan.typesTaken
            totCourses = taken[0] + taken[1] + taken[2] + taken [3] + taken[4] + taken[13]
            if curriculum == CS:
                if totCourses >= courseLimit or suggestedPlan.typesTaken[2] > 8:
                    continue
            else:
                if totCourses >= courseLimit or suggestedPlan.typesTaken[2] > 3:
                    continue

            # Only explore a plan if it has not been seen or it is a better plan than a previously seen version
            if str(suggestedPlan.coursesTaken) not in costSoFar or new_cost < costSoFar[str(suggestedPlan.coursesTaken)]:
                costSoFar[str(suggestedPlan.coursesTaken)] = new_cost
                priority = -new_cost + heuristics(suggestedCourseInfo, suggestedPlan, user)
                frontier.put(suggestedPlan, priority)

    print(curr_plan.typesTaken)
    return curr_plan.selectionsWithDay
# ======================================================================================================================
