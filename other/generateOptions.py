import getOptions
import filterOptions

def generateOptions(planStudent, dayToPrune, curriculum):
    list = getOptions.runQuery(planStudent)
    return filterOptions.filter(list, planStudent, dayToPrune, curriculum)
