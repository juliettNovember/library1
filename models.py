import sqlite3
from sqlite3 import Error

def create_connection(db_file):
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

if __name__ == '__main__':
    create_connection(r"database.db")

def execute_sql(conn, sql):
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


if __name__ == "__main__":
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

create_tasks_sql = """
-- zadanie table
CREATE TABLE IF NOT EXISTS tasks (
  id integer PRIMARY KEY,
  title text NOT NULL,
  description VARCHAR(250) NOT NULL,
  year integer,
  species text NOT NULL,
  watch text NOT NULL,
  FOREIGN KEY (projekt_id) REFERENCES projects (id)
);
"""

db_file = "database.db"

conn = create_connection(db_file)
if conn is not None:
    execute_sql(conn, create_projects_sql)
    execute_sql(conn, create_tasks_sql)
    conn.close()

def add_projekt(conn, projekt):
    """
    Create a new projekt into the projects table
    :param conn:
    :param projekt:
    :return: projekt id
    """
    sql = '''INSERT INTO projects(title, description, year, species, watch)
            VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, projekt)
    conn.commit()
    return cur.lastrowid

def add_zadanie(conn, zadanie):
    """
    Create a new zadanie into the tasks table
    :param conn:
    :param zadanie:
    :return: zadanie id
    """
    sql = '''INSERT INTO tasks(projekt_id, title, description, year, species, watch)
            VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, zadanie)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":
   projekt = ("Title", "Description", "Year", "Species", "Watch")

   conn = create_connection("database.db")
   pr_id = add_projekt(conn, projekt)

   zadanie = (
       pr_id,
       "Save Private Ryan",
       "War Drama",
       "1998",
       "Species",
       "True"
   )

   zadanie_id = add_zadanie(conn, zadanie)

   print(pr_id, zadanie_id)
   conn.commit()
