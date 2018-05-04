import search
from ManualOptionQuery import ManualOptionQuery
class DegreeBuilder:
    def __init__(self, Student, search_type):
        self.Student = Student
        self.search_type = search_type

    def runDegree(self):
        if self.search_type == 0:
           return self.automatedSearch(self.Student)
        else:
            return self.manualSearch()

    def automatedSearch(self):
        search.automated(self)

    def manualSearch(self):
        return ManualOptionQuery.runQuery(self)