cars = [
    ("volvo", 1995),
    ("mers", 2000),
    ("vaz", 2005),
    ("faw", 1988)
]

# Равнозначные запросы на вставку
# for car in cars:
#     cur.execut("INSERT INTO cars VALUES(NULL,?,?)",car)

# cur.executmany("INSERT INTO cars VALUES(NULL,?,?)",cars)

# cur.executescript("""DELETE FROM cars WHERE model LIKE 'A%',
#     UPDATE cars SET prise = prise+1000
# """)

# для выборки как словарь
# con.row_factory = sq.Row
# cur.execut("SELECT model, price FROM cars")
# for result in cur:
#     print(result['model'],result['price'])

# БЭК АП
# import sqlite3 as sq
#
# with sq.connect("cars.db") as con:
#     cur = con.cursor()
#     with open("sql_damp.sql", "w") as f:
#         for sql in con.interdump():
#             f.write(sql)

# import sqlite3 as sq
#
# with sq.connect("cars.db") as con:
#     cur = con.cursor()
#     with open("sql_damp.sql", "r") as f:
#         sql = f.read()
#         cur.executscript(sql)
