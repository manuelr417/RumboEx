from RumboEx.config.dbconfig import pg_config
import psycopg2


class CourseDAO:
    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    # GET Methods

    def get_courses_by_student_id(self, student_id):
        cursor = self.conn.cursor()

        query = 'select ' \
                'c.course_id, c.name, c.codification, c.credits, s.section_num, s.section_id, e.enrolled_id ' \
                'from ' \
                'enrolled as e  ' \
                'natural inner join course as c ' \
                'natural inner join section as s ' \
                'where e.student_id=%s;'
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_course_by_course_id(self, course_id):
        cursor = self.conn.cursor()
        query = "select * from course where course_id = %s;"
        cursor.execute(query, (course_id,))
        result = cursor.fetchone()
        if not result:
            return None
        return result

    def get_section_times_by_section_id(self, section_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                's.day, s.start_time, s.end_time ' \
                'from section_time as s ' \
                'where section_id=%s;'
        cursor.execute(query, (section_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_grades_by_course_id(self, enrolled_id):
        cursor = self.conn.cursor()
        query = 'select ' \
                'g.grade_id, g.name, g.grade, g.total, g.weight, g.date ' \
                'from ' \
                'grades as g natural inner join enrolled ' \
                'where enrolled.enrolled_id=%s;'
        cursor.execute(query, (enrolled_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    # POST Methods

    def insert_grade(self, name, grade, total, weight, date, student_id, course_id):
        cursor = self.conn.cursor()
        query1 = 'select e.enrolled_id from enrolled as e natural inner join section as s ' \
                 'where e.student_id=%s and s.course_id=%s;'
        cursor.execute(query1, (student_id, course_id, ))
        enrolled_id = cursor.fetchone
        query2 = 'insert into grades(name, grade, total, weight, date, enrolled_id) values (%s,%s,%s,%s,%s,%s) returning grade_id;'
        cursor.execute(query2, (name, grade, total, weight, date, enrolled_id, ))
        grade_id = cursor.fetchone
        return grade_id