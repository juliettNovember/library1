import json
import sqlite3
from sqlite3 import Error


class Todos:
    def __init__ (self):
        self.conn = self.create_connection("database.db")
        self.create_project()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)
        return conn

    # if __name__ == '__main__':
    #     create_connection(r"database.db")

    def execute_sql(self, conn, sql):
        """ Execute sql
        :param conn: Connection object
        :param sql: a SQL script
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)


    def create_project(self):
        create_projects_sql = """
        -- projects table
        CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        title text NOT NULL,
        description text,
        year integer,
        species text,
        watch text
        );
        """

        self.execute_sql(self.conn, create_projects_sql)

    def add_projekt(self, projekt):
        """
        Create a new projekt into the projects table
        :param conn:
        :param projekt:
        :return: projekt id
        """
        sql = '''INSERT INTO projects(id, title, description, year, species, watch)
            VALUES(?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, projekt)
        self.conn.commit()
        return cur.lastrowid


    def all(self):
        select_all_sql = "SELECT * FROM projects"
        cur = self.conn.cursor()
        cur.execute(select_all_sql)
        rows = cur.fetchall()
        return rows
    
    def one(self):
        select_one_sql = "SELECT * FROM projects"
        cur = self.conn.cursor()
        cur.execute(select_one_sql)
        rows = cur.fetchone()
        return rows

    def update(self):
        """
        update status, begin_date, and end date of a task
        :param conn:
        :param projekt:
        :return: projekt id
        """

        sql = '''UPDATE projects
        SET title = 'Intouchables',
            description = 'Touching story of a man helping a disabled person',
            year   = '2011',
            species = 'Biographical'
        WHERE id = 3;'''

        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return cur.lastrowid
    
    def delete(self):
        sql = '''DELETE FROM projects WHERE id = 3'''

        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return cur.lastrowid

        

    def get(self, id):
        return self.todos[id]
        todo = [todo for todo in self.all() if todo['id'] == id]
        if todo:
            return todo[0]
        return []

    def create(self, data):
        self.todos.append(data)
        self.save_all()

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

todos = Todos() 

# todos.add_projekt((3, "Save Private Ryan", "War Drama", 1998, "War Drama", "True"))

print(todos.delete())