class Student(object):
    previous_curriculum = ''
    def __init__(self, student_id, number_of_classes_per_quarter, courses_taken, current_quarter, curriculum, elective_preference):
       self.student_id = student_id
       self.number_of_classes_per_quarter = number_of_classes_per_quarter
       self.courses_taken = courses_taken
       self.current_quarter = current_quarter
       self.curriculum = curriculum
       self.elective_preference = elective_preference


    def addCourse(self, Course_ID):
        self.courses_taken.add(Course_ID)


    def deleteCourse(self, Delete_Course_ID):
        list = self.courses_taken
        for i in range(len(list)):
            if list[i] == Delete_Course_ID:
               self.courses_taken.remove(Delete_Course_ID)


    def changeQuarter(self, New_Quarter):
        self.current_quarter = New_Quarter


# TODO: Determine the type we want to use for the Quarter System
       # def changeQuarter(self):
        #    self.current_quarter += 5
        #  NOTE: Figure out how to format based onDatabase


    def changeElectivePreference(self, New_elective_preference):
        self.elective_preference = New_elective_preference


    def changeCurriculum(self, New_curriculum):
        Student.previous_curriculum = self.curriculum
        self.curriculum = New_curriculum


    def getPreviousCurriculum(self):
        return Student.previous_curriculum


    def getGradReqs(self):
        return self.curriculum.gradReqs

