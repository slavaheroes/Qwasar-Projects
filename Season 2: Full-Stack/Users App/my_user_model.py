import sqlite3

class User:

    def __init__(self, db_name):
        # create database
        self.sql = db_name
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()
        # create table
        c.execute(''' 
           create table if not exists Users(
               id integer PRIMARY KEY,
               firstname text NOT NULL,
               lastname text NOT NULL,
               age integer NOT NULL,
               password text NOT NULL,
               email text
           ) 
        ''')

        conn.commit()

        # nums will store the max id value so we can avoid repeated ids
        c.execute("select max(id) from Users")
        res = c.fetchall()
        if res[0][0]:
            self.nums = res[0][0]+1
        else:
            self.nums = 1
        

    def create(self, firstname, lastname, age, password, email):
        # create user id
        user_id = self.nums
        # increment number of users
        self.nums += 1

        # add to our database table
        query = '''
            insert into Users(id, firstname, lastname, age, password, email)
            values (?,?,?,?,?,?)
        '''
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()

        c.execute(query, (user_id, firstname, lastname, age, password, email))
        conn.commit()
        return user_id
    
    def get(self, user_id):
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()
        c.execute("select * from Users where id=?", (user_id,))
        row = c.fetchall()
        return row

    def all(self):
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()
        c.execute("select id, firstname, lastname, age, email from Users")
        rows = c.fetchall()
        return rows
    
    def update(self, user_id, attribute, value):
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()
        query = "update Users set {} = '{}' where id = {}".format(attribute, str(value), str(user_id))
        c.execute(query)
        conn.commit()

        return user_id
    
    def destroy(self, user_id):
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()
        c.execute("delete from Users where id = " + str(user_id))
        conn.commit()
    
    def sign_in(self, email, password):
        conn = sqlite3.connect(self.sql)
        c = conn.cursor()
        query = "select id from Users where email = '{}' and password = '{}' ".format(email, password)
        c.execute(query)
        res = c.fetchall()
        #print(res)
        if res:
            return res[0][0]
        else:
            return False




    


        
