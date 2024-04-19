import sqlite3 as sq


def sql_start(userid):

    base = sq.connect('users.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS Users_id (id INTEGER PRIMARY KEY)')
    cur.execute('INSERT INTO Users_id (id) VALUES (?)', (userid,))
    base.commit()
    base.close()


def count_id():
    base = sq.connect('users.db')
    cur = base.cursor()
    cur.execute('SELECT COUNT(*) FROM Users_id')
    total_users = cur.fetchone()[0]
    base.close()
    return total_users