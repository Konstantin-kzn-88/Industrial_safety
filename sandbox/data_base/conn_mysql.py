from mysql.connector import connect, Error

# конвертация в BLOB
def convertToBinaryData(self, file_path):
    with open(file_path, 'rb') as file:
        blobData = file.read()
    return blobData


# sql_insert_blob = """ INSERT INTO 'objects'
#                                     ('id', 'data', 'photo', 'name_photo') VALUES (?, ?, ?, ?)"""

try:
    with connect(
        host="server167.hosting.reg.ru",
        user="u1082920_test",
        password="!Fq3pKcK",
        database="u1082920_test",
    ) as con:
        cur = con.cursor()
        # Создать таблицу если ее не было
        cur.execute("""CREATE TABLE IF NOT  EXISTS foto (
            foto_id INTEGER PRIMARY KEY,
            pic BLOB
            )""")
        cur.execute("""SELECT * FROM foto""")
        result = cur.fetchall()
        print(result)
        con.commit()
        con.close()

except Error as e:
    print(e)

if __name__ == '__main__':
    print("start")