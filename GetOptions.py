import serialization
import Student
import psycopg2


'''
This will run a query to then return classes to the 
'''
def runQuery(StudentObject):
    print("Running Query")
#0975 Minumum Quarter Number
#1020 Maximum Quarter Number
    '''
    CODE COMMENTED OUT UNTIL OTHER PARTS ARE WORKING
    
    quarter_range = 45
    student_quarter = StudentObject.current_quarter
    if student_quarter <= 1020:
        quarter = student_quarter
    else:
        quarter = ((student_quarter % quarter_range) + 975)
'''

    dsn = "postgres://csc394:password@35.188.8.242:5432/csc394"
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    #TODO: Add the score when that has been placed into the DataBase
    cur.execute("SELECT c.subject, c.course_nbr, d.day  FROM csc394_courses c \
    INNER JOIN days_offered d ON (c.subject = d.subject AND c.course_nbr = d.catalog_nbr ) \
    WHERE d.stream = '0975' ORDER BY course_nbr")
    #TODO: ^^^^ Replace '0975' with %s and add , (va) at the end ^^^^
    row = cur.fetchone()

    i = 0
    while row is not None:
        subject = row[0]
        course_nbr = row[1]
        day = row[2]
        i = i + 1
        print(i,". ", subject, " ", course_nbr, " ", day )
        row = cur.fetchone()
    cur.close()


    return None