import os
import psycopg2
from psycopg2 import Error

def database_connection():
    connection = None
    try:
        connection = psycopg2.connect(user = "#####",
                                    password = "######",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "#####")
        cursor = connection.cursor()
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    # finally:
    #     #closing database connection.
    #         if(connection):
    #             cursor.close()
    #             connection.close()
    #             print("PostgreSQL connection is closed")
    return connection

def remember(note: str, user: str):
    conn = database_connection()
    cur = conn.cursor()

    cur.execute('''INSERT INTO remember('remember', 'slack_user') VALUES (%s,%s);'''%(note, user))
    cur.commit()
    cur.close()
