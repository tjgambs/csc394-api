class Student(object):
    previourMajor = ''
    def __init__(self, Student_ID, Number_of_Classes_per_Quarter, Courses_Taken, Current_Quarter, Option_Type, Major, Specialty):
       self.Student_ID = Student_ID
       self.Number_of_Classes_per_Quarter = Number_of_Classes_per_Quarter
       self.Courses_Taken = Courses_Taken
       self.Current_Quarter = Current_Quarter
       self.Option_Type = Option_Type
       self.Major = Major
       self.Specialty = Specialty


    def addCourse(self, Course_ID):
        self.Courses_Taken.append(Course_ID)

    def deleteCourse(self, Delete_Course_ID):
        list = self.Courses_Taken
        for i in range(len(list)):
            if list[i] == Delete_Course_ID:
               self.Courses_Taken.remove(Delete_Course_ID)

    def changeQuarter(self, New_Quarter):
        self.Current_Quarter = New_Quarter

       # def changeQuarter(self):
        #    self.Current_Quarter += 5
        #  NOTE: Figure out how to format based onDatabase!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def changeSpecialty(self, New_Specialty):
        self.Specialty = New_Specialty

    def changeMajor(self, New_Major):
        Student.previousMajor = self.Major
        self.Major = New_Major

    def getPreviousMajor(self):
        return Student.previousMajor

