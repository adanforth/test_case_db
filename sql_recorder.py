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


def create_condition(conn, condition):
    """
    Add a new condition into the condition table
    :param conn:
    :param condition:
    :return: condition id
    """
    sql = ''' INSERT INTO Conditions(condName, condDesc, screenshot)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, condition)
    conn.commit()
    return cur.lastrowid



def create_event(conn, event):
    """
    Create a new event
    :param conn:
    :param event:
    :return:
    """

    sql = ''' INSERT INTO Events(eventName, eventDesc, preID, postID)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, event)
    conn.commit()

    return cur.lastrowid

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def selectConditions(conn):
    """
    Query all rows in the conditions table
    :param conn: the connection object
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Conditions")

    return cur.fetchall()


def main():
    # db_dir = input("enter directory for database:\n")
    # db_name = (input("enter database name:\n")) + '.db'
    # database = os.path.join(db_dir, db_name)
    database = r'C:\Users\deand\OneDrive\Documents\sqlite\db\pythonsqlite.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        stop = False
        print('to exit, press \"ENTER\"')
        while(not stop):
            usrInput = input("Insert a new Condition(type \"c\")? Insert a new Event(type \"e\")?\n").lower()
            #create a new condition
            if usrInput == 'c':
                cN = input("Condition Name:\t")
                cD = input("Condition Description:\t")

                correctDir = False
                print('to exit, press \"ENTER\"')
                while(not correctDir):
                    scDir = input("screenshot directory:\t")
                    if scDir == '':
                        correctDir = True
                        scDir = None
                    elif path.exists(scDir):
                        correctDir = True
                        print("directory found!")
                    else:
                        print("sorry, that directory does not exist. try again")
                    try:
                        sc = convertToBinaryData(scDir)
                        condition = (cN, cD, sc);
                        condition_id = create_condition(conn, condition)
                        print('entry successfully inserted into the Conditions table under id ' + str(condition_id))
                    except:
                        print("Oops! there was an error inserting the data")

            elif usrInput == 'e':                
                eN = input("Event Name:\t")
                eD = input("Event Description:\t")
                print("Conditions:")
                for row in selectConditions(conn):      
                    print(row[0:3])
                isInt = False
                while(not isInt):
                    try:
                        preID = int(input("select precondition ID:\t"))
                        if preID > len(row):
                            raise Exception()
                        isInt = True
                    except:
                        print("sorry, enter a valid id please")
                isInt = False
                while(not isInt):
                    try:
                        postID = int(input("select postcondition ID:\t"))
                        if postID > len(row):
                            raise Exception()
                        isInt = True
                    except:
                        print("sorry, enter a valid id please")
                try:
                    event = (eN, eD, preID, postID);
                    event_id = create_event(conn, event)
                    print('entry succesfully inserted into the Events table under id ' + str(event_id))
                except:
                    print("Oops! there was an error inserting the data")
            elif usrInput == '':
                stop = True
                

if __name__ == '__main__':
    main()