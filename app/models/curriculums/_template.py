
class Curriculum(object):
    """Class represents a degree. Allows courses to be
    assigned to particular subtypes. Used in goal checking.
    """

    def __init__(self, intros=set(), foundations=set(), advCourses=set(),
                 openElects=set(), softDevs=set(), theorys=set(),
                 dataScis=set(), databases=set(), ais=set(), softEngs=set(),
                 gameRTSys=set(), humCompInts=set(), capstones=set(),
                 majElects=set(), gradReqs=[0, 0, 0, 0, 0, 0, 0]):
        self.gradReqs = gradReqs
        self.introductory_courses = intros
        self.foundation_courses = foundations
        self.advanced_courses = advCourses
        self.open_elective_courses = openElects
        self.software_systems_dev_courses = softDevs
        self.theory_courses = theorys
        self.data_science_courses = dataScis
        self.database_systems_courses = databases
        self.ai_courses = ais
        self.software_engineering_courses = softEngs
        self.game_and_real_time_systems_courses = gameRTSys
        self.human_computer_interaction_courses = humCompInts
        self.capstone_courses = capstones
        self.major_elective_courses = majElects
        self.courseTypeDesignations = [
            intros, foundations, majElects, openElects, capstones, softDevs, theorys,
            dataScis, databases, ais, softEngs, gameRTSys, humCompInts, advCourses]
        self.coursesInCurriculum = (
            intros | foundations | advCourses
            | openElects | softDevs | theorys | dataScis
            | databases | ais | softEngs | gameRTSys
            | humCompInts | capstones | majElects)
