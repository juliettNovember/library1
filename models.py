import json
import sqlite3
from sqlite3 import Error

class DataBaseError(Exception):
    pass


class Projects:

    def __init__(self):
        self.conn = self.create_connection("database.db")
        self.create_project()
        print("Polaczylo")

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

    def execute_sql(self, sql, data=None):
        """
        :param sql: a SQL script
        :param data: tuple
        :return: cursor object
        """
        try:
            cur = self.conn.cursor()
            if data:
                cur.execute(sql, data)
                self.conn.commit()
            else:
                cur.execute(sql)
            return cur
        except Error as e:
            raise DataBaseError(f"Akcja nie powiodła sie z powodu: {e}")

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

        self.execute_sql(create_projects_sql)

    def all(self):
        sql = "SELECT * FROM projects"
        projects = self.execute_sql(sql)
        return projects.fetchall()

    def details(self, id):
        sql = "SELECT * FROM projects WHERE id = ?"
        project = self.execute_sql(sql, (id,))
        return project.fetchone()

    def create(self, project):
        sql = "INSERT INTO projects(id, title, description, year, species, watch) VALUES(?,?,?,?,?,?)"
        try:
            self.execute_sql(sql, project)
            return project

        except DataBaseError as e:
            return [str(e)]

    def update(self, id, project):
        sql = """
        UPDATE projects
            SET title = ?,
                description = ?,
                year = ?,
                species = ?,
                watch = ?
                WHERE id = ?;"""
        data = project + (id, )
        cur = self.execute_sql(sql, data)
        return data

    def delete(self, id):
        sql = "DELETE FROM projects WHERE id = ?"
        self.execute_sql(sql, (id, ))
        return True

projects = Projects()

if __name__ == "__main__":
    print(projects.all())


