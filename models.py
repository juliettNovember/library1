import json
import sqlite3
from sqlite3 import Error
from flask import g

class DataBaseError(Exception):
    pass


class Movlib:
    def __init__(self):
        self.conn = self.create_connection("movie_database.db")
        self.create_movie_entry()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file, check_same_thread=False)
            conn.row_factory = sqlite3.Row
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

    def create_movie_entry(self):
        create_movlib_sql = """
        -- movlib table
        CREATE TABLE IF NOT EXISTS movlib (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title text NOT NULL,
        description text,
        year integer,
        species text,
        watch text
        );
        """

        self.execute_sql(create_movlib_sql)

    def all(self):
        sql = "SELECT * FROM movlib"
        movlib = self.execute_sql(sql)
        return movlib.fetchall()
        
    def details(self, id):
        sql = "SELECT * FROM movlib WHERE id = ?"
        project = self.execute_sql(sql, (id,))
        return project.fetchone()

    def create(self, project):
        if 'csrf_token' in project: del project['csrf_token']
        sql = "insert into movlib " + str(tuple(project.keys())) + " values " + str(tuple(project.values())) 
        print(sql)
        try:
            self.execute_sql(sql, project)
            self.execute_sql("insert into movlib ('id') values ('rowid')")
            return project
    
        except DataBaseError as e:
            return [str(e)]

    def update(self, id, project):
        sql = """
        UPDATE movlib
            SET title = ?,
                description = ?,
                year = ?,
                species = ?,
                watch = ?
                WHERE id = ?;"""
       
        data = project,id
        data = project['title'],project['description'],project['year'],project['species'],project['watch'], id
        self.execute_sql(sql, data)
        return data

    def delete(self, id):
        print("id:", id)
        #czasem pojawia sie blad "cannot start transaction in another transaction". dodanie tego commita w takiej sytuacji zakańcza otwartą tranzakcje.
        try:
            self.execute_sql("COMMIT")
        except DataBaseError:
            pass
        
        #ten kod tworzy na nowo tabele projects z poprawiona numeracja po usunieciu jednego z wierszy
        self.execute_sql("BEGIN TRANSACTION")
        sql = "DELETE FROM movlib WHERE id = ?"
        self.execute_sql(sql, (id, ))
        self.execute_sql("CREATE TEMPORARY TABLE movlib_backup(title, description, year, species, watch)")    
        self.execute_sql("INSERT INTO movlib_backup(title, description, year, species, watch) SELECT title, description, year, species, watch FROM movlib")
        self.execute_sql("DROP TABLE movlib")
        self.execute_sql("CREATE TABLE movlib(id INTEGER PRIMARY KEY, title text NOT NULL,description text,year integer,species text,watch text)")
        self.execute_sql("INSERT INTO movlib(title, description, year, species, watch) SELECT title, description, year, species, watch FROM movlib_backup")
        self.execute_sql("DROP TABLE movlib_backup")
        self.execute_sql("COMMIT")
        
        return True



movlib = Movlib()

if __name__ == "__main__":
    print(movlib.all())


