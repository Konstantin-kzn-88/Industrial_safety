# SELECT * FROM users WHERE score < 1000
# INSERT INTO users VALUES ('Mike',1,19,1000)
# INSERT INTO users (name,old,score) VALUES('Mike',19,1000)
# =,==, >, <, >=, <=, !=, BETWEEN
# SELECT * FROM users WHERE score BEETWEEN 500 AND 1000
# AND, OR, NOT, IN, NOT IN
# SELECT * FROM users WHERE score old>25 AND score<1000
# SELECT * FROM users WHERE score old>25 AND score<1000 OR sex =1
# ORDER BY old ASC (по возрастанию, после SELECT)
# ORDER BY old DESC (по убыванию, после SELECT)
# LIMIT 2 (сколько записей показать в выборке, после SELECT)
#
# Взять очки больше ста, показать первые 5 записей
# SELECT * FROM users
# WHERE score > 100 ORDER BY score DESC LIMIT 5

# Взять очки больше ста,  первые 5 записей, показать из кроме первых 2
# SELECT * FROM users
# WHERE score > 100 ORDER BY score DESC LIMIT 5 OFFSET 2

import sqlite3 as sq

with sq.connect("tst.db") as con:  # так
    cur = con.cursor()
    cur.execute("""SELECT * FROM users 
                WHERE score > 100 
                ORDER BY score DESC LIMIT 5""")
    result = cur.fetchall()  # вернуть список всех данных
    # fetchone - первая запись
    # fetchmany(2) - первые 2 записи
    print(result)

if __name__ == '__main__':
    pass
