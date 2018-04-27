class Curriculum:
    'class represents a degree. Allows courses to be assigned to particular subtypes. This will be used in goal checking.'

    def __init__(self, courseTypeDesignations, reqs):
        self.introductory_courses = courseTypeDesignations[0]
        self.foundation_courses = courseTypeDesignations[1]
        self.major_elective_courses = courseTypeDesignations[2]
        self.open_elective_courses = courseTypeDesignations[3]
        self.capstone_courses = courseTypeDesignations[4]
        self.software_systems_dev_courses = courseTypeDesignations[5]
        self.theory_courses = courseTypeDesignations[6]
        self.data_science_courses = courseTypeDesignations[7]
        self.database_systems_courses = courseTypeDesignations[8]
        self.ai_courses = courseTypeDesignations[9]
        self.software_engineering_courses = courseTypeDesignations[10]
        self.game_and_real_time_systems_courses = courseTypeDesignations[11]
        self.human_computer_interaction_courses = courseTypeDesignations[12]

        self.gradReqs = reqs


    # Sets of courseID numbers that will count for a particular type of course
    introductory_courses = set()
    foundation_courses = set()
    major_elective_courses = set()
    open_elective_courses = set()
    software_systems_dev_courses = set()
    theory_courses = set()
    data_science_courses = set()
    database_systems_courses = set()
    ai_courses = set()
    software_engineering_courses = set()
    game_and_real_time_systems_courses = set()
    human_computer_interaction_courses = set()
    capstone_courses = set()

    # Indexes correspond to the number of intro, foundation, major electives, open electives, capstones, and courses from a single concentration required for graduation
    gradReqs = [0, 0, 0, 0, 0, 0]
