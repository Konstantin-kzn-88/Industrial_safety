from mysql.connector import connect, Error

try:
    with connect(
        host="server167.hosting.reg.ru",
        user="u1082920_default",
        password="!Fq3pKcK",
    ) as connection:
        print(connection)
except Error as e:
    print(e)

if __name__ == '__main__':
    print("start")