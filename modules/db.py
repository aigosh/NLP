from sqlite3 import connect, Connection
from os.path import isfile
from typing import List


def create_db(path: str, table_name: str):
    if not isfile(path):
        file = open(path, 'w')

    db = connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS {} (url text, title text, description text)".format(table_name))

    return db


def write_pages(db: Connection, table_name, pages: List[tuple]):
    for page in pages:
        (url, title, description) = page
        db.execute('INSERT INTO {} VALUES (?,?,?)'.format(table_name), (url, title, description))


def read_pages(db: Connection, table_name: str):
    return db.execute("SELECT * FROM {}".format(table_name)).fetchall()
