import sqlite3
from sqlite3 import Error

# creates a sqlite database with tables for events and conditions
def create_connection(db_file):
    #create a database connection to a SQLite database 
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"C:\Users\deand\OneDrive\Documents\sqlite\db\pythonsqlite.db"

    sql_create_conditions_table = """ CREATE TABLE IF NOT EXISTS Conditions (
                                        "condID"	integer UNIQUE,
                                        "condName"	text NOT NULL,
                                        "condDesc"	text,
                                        "screenshot"	BLOB,
                                        PRIMARY KEY("condID")
                                    ); """

    sql_create_events_table = """ CREATE TABLE IF NOT EXISTS Events (
                                        "eventID"	integer UNIQUE,
                                        "eventName"	text NOT NULL,
                                        "eventDesc"	text,
                                        "preID"	INTEGER NOT NULL,
                                        "postID"	INTEGER NOT NULL,
                                        PRIMARY KEY("eventID"),
                                        FOREIGN KEY("postID") REFERENCES "Conditions"("condID"),
                                        FOREIGN KEY("preID") REFERENCES "Conditions"("condID")
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create conditions table
        create_table(conn, sql_create_conditions_table)

        # create events table
        create_table(conn, sql_create_events_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
    


