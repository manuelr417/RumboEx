import psycopg2
from RumboEx.config.dbconfig import pg_config


class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (
        pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['host'], pg_config['port'])
        self.conn = psycopg2.connect(connection_url)

    # GET Methods

    def getUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'select id, username, name, lastname, email, password from "user" where id=%s;'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if not result:
            return None
        return result

    def getMentorsByStudentId(self, student_id):
        cursor = self.conn.cursor()
        query = 'select u.id, u.username, u.name, u.lastname, u.email, ' \
                'r.id as role_id, r.name as role_name ' \
                'from "user" as u inner join mentors_students as m on u.id=m.mentor_id ' \
                'inner join users_roles as ur on ur.user_id=u.id ' \
                'inner join role as r on r.id=ur.role_id ' \
                'where m.student_id=%s;'
        cursor.execute(query,(student_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # POST Methods

    def insertCounselor(self, username, email, password, name, lastname):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        # self.conn.commit()
        query2 = 'insert into counselor(user_id) values(%s); ' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name=%s));'
        cursor.execute(query2, (user_id, user_id, 'counselor'))
        self.conn.commit()
        return user_id

    def insertPsychologist(self, username, email, password, name, lastname):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        # self.conn.commit()
        query2 = 'insert into psychologist(user_id) values(%s); ' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name=%s));'
        cursor.execute(query2, (user_id, user_id, 'psychologist'))
        self.conn.commit()
        return user_id

    def insertAdvisor(self, username, email, password, name, lastname):
        cursor = self.conn.cursor()
        query = 'insert into "user"(username, email, password, name, lastname) values(%s, %s, %s, %s, %s) returning id;'
        cursor.execute(query, (username, email, password, name, lastname))
        user_id = cursor.fetchone()[0]
        # self.conn.commit()
        query2 = 'insert into advisor(user_id) values(%s); ' \
                 'insert into users_roles(user_id, role_id) values (%s, ' \
                 '(select id from role where name=%s));'
        cursor.execute(query2, (user_id, user_id, 'advisor'))
        self.conn.commit()
        return user_id

    # PUT Methods

    def changeEmail(self, user_id, email):
        cursor = self.conn.cursor()
        query = 'update "user" set email = %s where id = %s returning id, email as new_email;'
        cursor.execute(query,(email,user_id,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def changeUsername(self, user_id, username):
        cursor = self.conn.cursor()
        query = 'update "user" set username = %s where id = %s returning id, username as new_username;'
        cursor.execute(query,(username,user_id,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def changePassword(self, user_id, password):
        cursor = self.conn.cursor()
        query = 'update "user" set password = %s where id = %s returning id;'
        cursor.execute(query,(password,user_id,))
        result = cursor.fetchone()
        self.conn.commit()
        return result
