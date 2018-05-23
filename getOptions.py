import serialization
import Student
import psycopg2
import ast


'''
This will run a query to then return classes to the 
'''
def runQuery(planStudent):
    print("Running Query")
#0975 Minumum Quarter Number
#1020 Maximum Quarter Number

    quarter_range = 45
    student_quarter = planStudent #planStudent.termNum
    if student_quarter <= 1020:
        quarter = student_quarter
    else:
        quarter = ((student_quarter % quarter_range) + 975)

    if quarter < 1000:
        stream = '0'+str(quarter)
    else:
        stream = str(quarter)

    query = "SELECT c.subject, c.course_nbr, d.day, c.score, c.prereqs FROM csc394_courses c \
    INNER JOIN days_offered d ON (c.subject = d.subject AND c.course_nbr = d.catalog_nbr ) \
    WHERE d.stream = '" +stream+ "' ORDER BY score DESC"

    dsn = "postgres://csc394:password@35.188.8.242:5432/csc394"
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchone()
    ''' cur.execute("SELECT c.subject, c.course_nbr, d.day, c.score, c.prereqs FROM csc394_courses c \
       INNER JOIN days_offered d ON (c.subject = d.subject AND c.course_nbr = d.catalog_nbr ) \
       WHERE d.stream = '0975' ORDER BY score DESC")
       '''

    i = 0
    array = []
    classes = []
    while row is not None:

        subject = row[0]
        #classes.append(subject)
        course_nbr = row[1]
        classes.append(subject + " " + str(course_nbr))
        day = row[2]
        classes.append(day)
        score = row[3]
        classes.append(score)
        pre = row[4]
        classes.append(pre)
        parseString(pre)
        row = cur.fetchone()
        array.append(classes)
        classes = []
    cur.close()


    return array

def parseString (string):
    string = "([CSC 453, CSC 451, CSC 455], [CSC 401, IT 411])"
    for index in range(len(string)):






'''
string = string.lower().split("[]")
string = string[0].split("()")
string = string[0].split(",")
string = string[0].split("[]")
string = string[0].split(",")

for index in range(len(string)):
    if string.startswith("[", index , len(string)):
        print("true")'''

# print(list)
