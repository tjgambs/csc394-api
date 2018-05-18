# TODO: Find actual course_IDs for required courses and add them to appropriate sets

# This section creates a Curriculum object for the Computer Science master's program.
# CourseID numbers that satisfy specific class types in a curriculum. The following sets will allow the search to recognize the type of class it is looking at in order to properly count totals for goal checking
csIntros = {34213, 34215, 34278, 34218, 34220, 34575}
csFoundations = {33962, 33968, 33970, 34721, 34736}
csOpenElects = set{}
csSoftDevs = {'csc436', 'csc438', 'csc439', 'csc443', 'csc448', 34678, csc462, csc471, csc472, csc475, csc534, 34223, csc540,
              csc548, csc549, csc551, csc552, csc553, csc595, cns450, gam690, gam 691, hci441, se441, 33885, se459,
              se525, se526, se554, se560, se491, 33893, tdc478, tdc484, 34529}
csTheorys = {csc431, csc440, csc444, csc489, csc503, 33983, csc525, csc531, csc535, csc547, csc557, csc580, csc591,
             se553}
csDataScis = {csc423, csc424, csc433, csc465, csc478, csc481, csc482, csc495, csc529, csc555, csc575, csc578, csc594,
              csc598, csc672}
csDatabases = {33973, csc454, csc478, csc529, csc543, csc549, csc551, csc553, 34650, 34325, csc575, csc589}
csAIs = {csc457, csc458, csc478, 35757, csc481, csc482, csc495, 34646, csc529, csc538, csc575, csc576, 35759, csc578,
         csc583, csc587, csc592, 34592, ect584, geo441, geo442, is467}
csSoftEngs = {se430, 33874, se441, 33884, se453, se456, 34632, se459, se475, 33889, se480, se482, se491, se525, se526,
              se529, se533, se546, se549, se554, se556, se560, se579, se581, se582, 33893}
csGameRTSys = {34678, csc462, 36252, 36259, gam425, 34714, gam453, gam470, gam475, gam476, gam486, gam575, 36257,
               gam690, 34189, gph436, gph469, gph570, gph572, gph580, se456}
csHumCompInts = {csc436, csc438, csc465, csc471, csc472, 34690, csc492, 34167, hci441, 34165, 34171}
csCourseDesignations = [csIntros, csFoundations, csMajElects, csOpenElects, csSoftDevs, csTheory, csDataScis,
                        csDatabases, csAIs, csSoftEngs, csGameRTSys, csHumCompInts]
csCapstones = set()
csMajElects = csSoftDevs.union(csTheorys).union(csDataScis).union(csDatabases).untion(csAIs).union(csSoftEngs).union(csGameRTSys).union(csHumCompInts)
csGradReqs = [6, 5, 8, 0, 0, 4]

CS = Curriculum(csCourseDesignations, csGradReqs)
