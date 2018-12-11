import os

import psycopg2
import psycopg2.extras
from flask import g

# Jake
data_source_name = 'host=faraday.cse.taylor.edu dbname=camp_bank user=camp_bank password=03059710'

# This is for testing. Use the above value unless an environment
# variable called 'DSN' is defined.
data_source_name = os.environ.get('DSN', data_source_name)
print("DSN is {}".format(data_source_name))


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


def add_camper(name, swim_number, prompt):
    query = '''
    INSERT INTO "camper" (name, swim_number, prompt)
    VALUES (%(name)s, %(swim_number)s, %(prompt)s)'''
    g.cursor.execute(query, {'name': name, 'swim_number': swim_number, 'prompt': prompt})
    g.connection.commit()
    return g.cursor.rowcount


def get_camper(id):
    query = '''
    SELECT *
    FROM "camper"
    WHERE camper.id = %(id)s'''
    g.cursor.execute(query, {'id': id})
    return g.cursor.fetchone()


def get_session(id):
    query = '''
    SELECT description
    FROM session
    WHERE session.id = %(id)s'''
    g.cursor.execute(query, {'id': id})
    return g.cursor.fetchone()


def load_camper(swim_number):
    query = '''
    SELECT camper.id
    FROM "camper"
    INNER JOIN session ON camper.session_id = session.id
    WHERE camper.swim_number = %(swim_number)s AND session.active = TRUE'''
    g.cursor.execute(query, {'swim_number': swim_number})
    return g.cursor.fetchone()


def post_transaction(camper_id, time, item_id, amount):
    query = '''
    INSERT INTO "transaction" (camper_id, time, item_id, amount)
    VALUES (%(camper_id)s, %(time)s, %(item_id)s,%(amount)s)'''
    g.cursor.execute(query, {'camper_id': camper_id, 'time': time, 'item_id': item_id, 'amount': amount})
    return g.cursor.rowcount


def find_transactions(id):
    query = '''
    SELECT *
    FROM transaction
    INNER JOIN transaction ON transaction.camper_id = camper.id
    WHERE camper.id = %(id)s'''
    g.cursor.execute(query, {'id': id})
    return g.cursor.fetchall()


def add_session(description, active):
    query = '''
    INSERT INTO "session" (description, active)
    VALUES (%(description)s, %(active)s)'''
    g.cursor.execute(query, {'description': description, 'active': active})
    return g.cursor.rowcount


def get_sessions():
    query = '''SELECT * FROM "session"'''
    g.cursor.execute(query)
    return g.cursor.fetchall()
