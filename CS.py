import Curriculum

# This section creates a Curriculum object for the Computer Science master's program.
# Course names that satisfy specific class types in a curriculum. The following sets will allow the search to recognize
# the type of class it is looking at in order to properly count totals for goal checking

intros = {'csc400', 'csc401', 'csc402', 'csc403', 'csc406', 'csc407'}

foundations = {'csc421', 'csc435', 'csc447', 'csc453', 'se450'}

advCourses = {}

openElects = set{}

softDevs = {'csc436', 'csc438', 'csc439', 'csc443', 'csc448', 'csc461', 'csc462', 'csc471', 'csc472', 'csc475', 'csc534', 'csc536', 'csc540',
              'csc548', 'csc549', 'csc551', 'csc552', 'csc553', 'csc595', 'cns450', 'gam690', 'gam691', 'hci441', 'se441', 'se452', 'se459',
              'se525', 'se526', 'se554', 'se560', 'se491', 'se591', 'tdc478', 'tdc484', 'tdc568'}

theorys = {'csc431', 'csc440', 'csc444', 'csc489', 'csc503', 'csc521', 'csc525', 'csc531', 'csc535', 'csc547', 'csc557', 'csc580', 'csc591',
             'se553'}

dataScis = {'csc423', 'csc424', 'csc433', 'csc465', 'csc478', 'csc481', 'csc482', 'csc495', 'csc529', 'csc555', 'csc575', 'csc578', 'csc594',
              'csc598', 'csc672'}

databases = {'csc433', 'csc452', 'csc454', 'csc478', 'csc529', 'csc543', 'csc549', 'csc551', 'csc553', 'csc554', 'csc555', 'csc575', 'csc589'}

ais = {'csc457', 'csc458', 'csc478', 'csc480', 'csc481', 'csc482', 'csc495', 'csc528', 'csc529', 'csc538', 'csc575', 'csc576', 'csc577', 'csc578',
         'csc583', 'csc587', 'csc592', 'csc594', 'ect584', 'geo441', 'geo442', 'is467'}

softEngs = {'se430', 'se433', 'se441', 'csc452', 'se453', 'se456', 'se457', 'se459', 'se475', 'se477', 'se480', 'se482', 'se491', 'se525', 'se526',
              'se529', 'se533', 'se546', 'se549', 'se554', 'se556', 'se560', 'se579', 'se581', 'se582', 'se591'}

gameRTSys = {'se461', 'csc462', 'csc486', 'csc588', 'gam425', 'gam450', 'gam453', 'gam470', 'gam475', 'gam476', 'gam486', 'gam575', 'gam576',
               'gam690', 'gam691', 'gph436', 'gph469', 'gph570', 'gph572', 'gph580', 'se456'}

humCompInts = {'csc436', 'csc438', 'csc465', 'csc471', 'csc472', 'csc491', 'csc492', 'hci440', 'hci441', 'hci430', 'hci454'}

capstones = set()

majElects = softDevs.union(theorys).union(dataScis).union(databases).union(ais).union(softEngs).union(gameRTSys).union(humCompInts)

courseDesignations = [intros, foundations, majElects, openElects, softDevs, theorys, dataScis,
                        databases, ais, softEngs, gameRTSys, humCompInts, advCourses]

gradReqs = [6, 5, 8, 0, 0, 4, 0]

# Actually create the Curriculum object representing the Computer Science program (CS)
CS = Curriculum(courseDesignations, gradReqs)
