from flask import g, flash, session
import psycopg2
import psycopg2.extras
# import info

# Database tools
data_source_name = 'host=faraday.cse.taylor.edu db_name=camp_bank password=03059710'

# 23 Functions to test



####OPEN AND CLOSE DATABASE####
def connect():
    '''
    Open a connection to the database.
    Will open a connection to the data_source_name path.
    Stores resulting connection in g
    :return:'''
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def disconnect():
    '''
    Closes connection to database.

    Properly discards all tools used.
    :return:
    '''

    g.cursor.close()
    g.connection.close()


def add_camper(name, prompt):
    query = '''
    INSERT INTO "camper" (name, prompt)
    VALUES (%(name)s, %(prompt)s)'''
    g.cursor.execute(query, {'name': name, 'prompt': prompt})
    g.connection.commit()
    return g.cursor.rowcount


