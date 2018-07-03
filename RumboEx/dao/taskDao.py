from RumboEx.config.dbconfig import pg_config
import psycopg2


class TaskDAO:
    def __init__(self):

        connection_url = "host=%s dbname=%s user=%s password=%s" % (pg_config['hostname'],
                                                                    pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['password'])
        self.conn = psycopg2._connect(connection_url)

    # GET Methods

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        query = "select * from task;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_personal_tasks(self):
        cursor = self.conn.cursor()
        query = "select * from task natural inner join personal_task;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_study_tasks(self):
        cursor = self.conn.cursor()
        query = "select * from task natural inner join study_task;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_course_tasks(self):
        cursor = self.conn.cursor()
        query = "select * from task natural inner join course_task;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_tasks_by_student_id(self, student_id):
        cursor = self.conn.cursor()
        query = "select * from task natural inner join student_tasks where student_id = %s;"
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_personal_tasks_by_student_id(self, student_id):
        cursor = self.conn.cursor()
        # el natural inner join for some reason no lo coje entre task t personal_task
        query = "select * from task inner join personal_task using(task_id) natural inner join student_tasks where student_id = %s;"
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_study_tasks_by_student_id(self, student_id):
        cursor = self.conn.cursor()
        query = "select * from task inner join study_task using(task_id) natural inner join student_tasks where student_id = %s;"
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    def get_course_tasks_by_student_id(self, student_id):
        cursor = self.conn.cursor()
        query = "select * from task inner join course_task using (task_id) natural inner join student_tasks where student_id = %s;"
        cursor.execute(query, (student_id,))
        result = []
        for row in cursor:
            result.append(row)
        if not result:
            return None
        return result

    # POST Methods

    def add_task(self, name, description, start_time, end_time, status):
        cursor = self.conn.cursor()
        query = "insert into task(name, description, start_time, end_time, status) values (%s, %s, %s, %s, False) returning task_id;"
        cursor.execute(query, (name, description, start_time, end_time, status,))
        task_id = cursor.fetchone()
        return task_id

    def add_personal_task(self, name, description, start_time, end_time, status):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into personal_task(task_id) values (%s);"
        cursor.execute(query, (task_id,))
        return task_id

    def add_study_task(self, name, description, start_time, end_time, status, course_id):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into study_task(task_id, course_id) values (%s, %s);"
        cursor.execute(query, (task_id, course_id,))
        return

    def add_course_task(self, name, description, start_time, end_time, status, course_id):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into course_task(task_id, course_id) values (%s, %s);"
        cursor.execute(query, (task_id, course_id,))
        return

    def add_appointment_task(self, name, description, start_time, end_time, status):
        cursor = self.conn.cursor()
        task_id = self.add_task(name, description, start_time, end_time, status)
        query = "insert into appointment_task(task_id) values (%s);"
        cursor.execute(query, (task_id,))
        return