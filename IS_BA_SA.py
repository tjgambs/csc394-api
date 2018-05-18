import Curriculum

# This section creates a Curriculum object for the IS master's program with the
# Business Analysis / Systems Analysis Concentration.

# Course names that satisfy specific class types in a curriculum. The following sets will allow the search to recognize
# the type of class it is looking at in order to properly count totals for goal checking

intros = {}

foundations = {'is421', 'csc451', 'is422', 'is430'}

advCourses = {'cns440', 'is435', 'is485', 'is535', 'is560'}

openElects = set{}

softDevs = {}

theorys = {}

dataScis = {}

databases = {}

ais = {}

softEngs = {}

gameRTSys = {}

humCompInts = {}

capstones = set()

majElects = {'ect424', 'is444', 'ect480', 'is483', 'hci440', 'is431', 'is440', 'is455','is540', 'is556', 'is565', 'is578'}

courseDesignations = [intros, foundations, majElects, openElects, softDevs, theorys, dataScis,
                        databases, ais, softEngs, gameRTSys, humCompInts]

gradReqs = [5, 4, 2, 1, 1, 0]

# Actually create the Curriculum object representing the Information Science - Business Analysis / Systems Analysis program (CS)
CS = Curriculum(courseDesignations, gradReqs)
