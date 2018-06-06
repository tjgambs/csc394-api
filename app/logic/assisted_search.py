from app.models.plan import Plan
from app.models.term_courses import TermCourses
from app.logic.filterOptions import manualFilter
from app.models.curriculums import CS
from operator import itemgetter, attrgetter
from functools import wraps
from flask import Blueprint, jsonify, request, abort, g
from app.utils import prepare_json_response
from app.models.user import User
from app import app, db, auth, basicauth

import copy

def isGoal(plan, curriculum, courseLimit, userPref):
    types = plan.typesTaken
    if curriculum.introductory_courses      <= plan.coursesTaken \
        and curriculum.foundation_courses   <= plan.coursesTaken \
        and curriculum.gradReqs[2]          <= plan.typesTaken[2] \
        and curriculum.gradReqs[3]          <= plan.typesTaken[3] \
        and curriculum.gradReqs[4]          <= plan.typesTaken[4] \
        and curriculum.gradReqs[6]          <= plan.typesTaken[13]\
        and types[0] + types[1] + types[2]  <  courseLimit:      # Max classes in a plan


        # If plan includes the number of courses in preferred bucket to graduate return True
        if plan.typesTaken[userPref]:
            if curriculum.gradReqs[5]       <= plan.typesTaken[userPref]:
                return True
    else:
        return False

def addPrefBonus(csFocus, wishList, queryResults, term, curriculum):
        for row in queryResults[term]:
            if row.getName in curriculum.courseTypeDesignations[csFocus]:
                row.score += 20
            if row.getName in wishList:
                row.score += 20
            queryResults[term] = sorted(queryResults[term], key=attrgetter('score'), reverse=True)
        return queryResults


def assisted(user):
#def assisted():
    returnList = []
    # Collection front end information
    term = request.json.get('term')
    #term = '1005'
    coursesTaken = request.json.get('coursesTaken')
    #coursesTaken = set()
    curriculum = user.getCurriculum
   # curriculum = CS
    wishList = request.json.get('wishList')
    #wishList = set()

    getCSFocus = 5

    # Querying results to be looked at
    # 1. Converting term to a searchable term
    # 2. Querying results and adding them to a dictionary
    # 3. Adding user requested bonuses
    currentTerm = TermCourses.convert_stream(term)
    queryResults = {term : TermCourses.getAvailableCourses(currentTerm)}
    queryResults = addPrefBonus(user.getCSFocus, wishList, queryResults, term, user.curriculum)
    #queryResults = addPrefBonus(getCSFocus, wishList, queryResults.copy(), term, curriculum)

    #create an empty plan to add all the courses taken and the buckets they are part of
    current_plan = Plan(
        selectionOrder = list(),
        coursesTaken = coursesTaken,
        #termNum = user.getTerm,
        termNum = term,
        currTermIdx = 0,
        maxCourses = len(coursesTaken),
        typesTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        selectionsWithDay = list())

    #All the courses taken (from the user) are assigned to an appropriate bucket.
    for i in range(len(coursesTaken)):
        classifyCourse = current_plan.classifyCourse(current_plan.cousesTaken[i])
        current_plan.incrCourseType(classifyCourse, current_plan.typesTaken, curriculum.gradReqs)
    #Checking if the Goal State is reached. If the State is reached then
    if isGoal(current_plan, curriculum, len(coursesTaken), user.getCSFocus):
    #if isGoal(current_plan, curriculum, len(coursesTaken), getCSFocus):
        return returnList

    #The Query results are then filtered
    filteredResults = manualFilter(queryResults[term], current_plan, current_plan.daysFilled, curriculum)

    #Selecting the Top 8 resutls to return
    endList = []

    for i in range(0, 8):
        course =  (filteredResults[i].getName, filteredResults[i].day)
        endList.append(course)

    returnList.append(endList)

    return returnList
