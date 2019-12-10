import sqlite3


class DBConnection:
    __instance = None
    connections = []

    def __init__(self):
        pass

    def __new__(cls):
        if not DBConnection.__instance:
            DBConnection.__instance = super().__new__(cls)
        return DBConnection.__instance

    def connect_to_db(self, dbname):
        try:
            return sqlite3.connect(dbname)
        except Exception as e:
            print(e)

    def db_query(self, dbcursor, query):
        try:
            dbcursor.execute(query)
            return True
        except:
            print(query)
            print('false')
            return False

    def db_query_many(self, dbcursor, query, myList):
        try:
            print('added')
            dbcursor.executemany(query, myList)
            return True
        except:
            print('not added')
            return False

    def add_query(self, dbcursor, query, myList):
        try:
            dbcursor.executemany(query, myList)
            return True
        except:
            return False

    def create_table(self, cursor, name, *fields):
        fd = ""
        for field in fields:
            fd += (field + ", ")
        self.db_query(cursor, 'CREATE TABLE IF NOT EXISTS {}({})'.format(name, fd[:-2]))

    def search(self, cursor, value, table, options=None):
        try:
            query = 'SELECT {} FROM {} {}'.format(value, table, options)
            self.db_query(cursor, query)
            return cursor.fetchall()
        except:
            return False

    def update(self, cursor, table, values, options=None):
        try:
            query = 'UPDATE {} SET {} {}'.format(table, values, options)
            if not options:
                query = query[:-5]
            self.db_query(cursor, query)
            return True
        except:
            return False
'''
db = DBConnection()
conn = db.connect_to_db('db2.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(name VARCHAR(255) PRIMARY KEY, age integer CHECK(age > 15), gender BOOLEAN , country VARCHAR(255))")

users_list1 = [('Gholii', 19, True), ('Sara', 28, False)]
# cursor.executemany(
#     "INSERT INTO users(name, age, gender)  VALUES(?, ?, ?)", users_list1)
query = "INSERT INTO users(name, age, gender)  VALUES(?, ?, ?)"
dbQuery = db.db_query_many(cursor, query, users_list1)
if dbQuery:
    print('dbQuery')
    conn.commit()
dbquery = db.db_query(cursor, 'SELECT * FROM users')
if dbquery:
    user_db_list = cursor.fetchall()

conn.close()

for user in user_db_list:
    print(user)
'''


