import sqlite3
from sqlite3 import Error
import os.path
from os import path






def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def selectConditions(conn):
    """
    Query all rows in the conditions table
    :param conn: the connection object
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Conditions")

    return cur.fetchall()

def selectEvents(conn):
    """
    Query all rows in the events table
    :param conn: the connection object
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Events")

    return cur.fetchall()

def stepThru(conditions, events):
    """
    Creating a Dictionary for events
    :key: precondition ID
    :value: event 'object' (it's really just a tuple containing the information)
    """
    e = {}
    for event in events:
        eventPreID = event[3]
        if not eventPreID in e.keys():
            e[eventPreID] = {}
            e[eventPreID][event[0]] = event
        else:
            e[eventPreID][event[0]] = event
    
    start = input("start stepping through conditions? y/n\n")
    stop = True
    if start == 'y':
        stop = False
        for row in conditions:      
            print(row[0:3])
        isInt = False
        while(not isInt):
            try:
                curID = int(input("select start condition ID:\t"))
                if curID > len(conditions):
                    raise Exception()
                isInt = True
            except:
                print("sorry, enter a valid id please")
    elif start == 'n':
        print("exiting program")
    
    while not stop:
        if curID in e.keys():
            print("the following are events that follow from the current condition: ")
            for event in e[curID]:
                print(e[curID][event])
            eventID = int(input("select the eventID you want to continue to (or press ENTER to quit)\t"))
            if not eventID in e[curID].keys():
                print("sorry, this event is not on the list")
                break
            if eventID == '':
                print("exiting program")
                break
            print("selected event: " + str(e[curID][eventID]))
            print("assuming success event, the next condition is: " + str(conditions[e[curID][eventID][4]][0:3]))
            curID = e[curID][eventID][4]
        else:
            print("sorry, there are no events leading from this condition")
            break


            

        

def main():
    # db_dir = input("enter directory for database:\n")
    # db_name = (input("enter database name:\n")) + '.db'
    # database = os.path.join(db_dir, db_name)
    database = r'C:\Users\deand\OneDrive\Documents\sqlite\db\pythonsqlite.db'
    # create a connection to the DB
    conn = create_connection(database)
    # fetch a list of the conditions from the DB
    conditions = selectConditions(conn)
    # fetch a list of the events from the DB
    events = selectEvents(conn)

    stepThru(conditions, events)
    

if __name__ == '__main__':
    main()



