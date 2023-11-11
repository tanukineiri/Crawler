import constants
import sqlite3

connection = None
cursor = None

def open_db():
    connection = sqlite3.connect(constants.db_name)
    cursor = connection.cursor()
    if cursor is not None:
        init_db()

def close_db():
    if connection is not None:
        connection.close()

def saveItem(name, phone, site, emails, errors):
    if (cursor is not None) and (connection is not None):
        cursor.execute('INSERT INTO InteriorDesign (name, phone, site, emails, errors)', (name, phone, site, emails, errors))
        connection.commit()

def init_db():
    if cursor is not None:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS InteriorDesign (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        site TEXT NOT NULL,
        emails TEXT NOT NULL,
        errors TEXT
        )
        ''')
