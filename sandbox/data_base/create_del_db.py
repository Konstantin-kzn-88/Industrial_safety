import sqlite3 as sq

with sq.connect("tst.db") as con:  # так
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users")  # del table if she be

    cur.execute("""CREATE TABLE IF NOT  EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sex INTEGER NOT NULL DEFAULT 1,
        old INTEGER,
        score INTEGER
        )""")

if __name__ == '__main__':
    pass
