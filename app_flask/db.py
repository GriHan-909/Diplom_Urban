import sqlite3

DATABASE = 'users.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL,
                height INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                gender TEXT NOT NULL
            )
        ''')


def add_user(name, age, height, weight, gender):
    conn = get_db()
    with conn:
        conn.execute('INSERT INTO users (name, age, height, weight, gender) VALUES (?, ?, ?, ?, ?)',
                     (name, age, height, weight, gender))


def get_user(name):
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE name = ?', (name,)).fetchone()
    return user


def del_user(name):
    conn = get_db()
    with conn:
        conn.execute('DELETE FROM users WHERE name = ?', (name,))
