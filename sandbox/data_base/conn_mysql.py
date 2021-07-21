from mysql.connector import connect, Error
import time


start = time.process_time()
file_path = 'C:\\Users\\konstantin\\Desktop\\test_in.png'
file_path_out = 'C:\\Users\\Konstantin_user\\Desktop\\test_out.png'

# конвертация в BLOB
def convertToBinaryData(file_path):
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
        # cur.execute("DROP TABLE IF EXISTS foto")  # del table if she be
        # Создать таблицу если ее не было
        cur.execute("""CREATE TABLE IF NOT  EXISTS foto (
            foto_id INTEGER,
            pic LONGBLOB
            )""")

        cur.execute("""SELECT * FROM foto""")
        result = cur.fetchall()
        # print(result[0][1])
        fout = open(file_path_out, 'wb')
        fout.write(result[0][1])
        fout.close()

        # запрос на добавление данных
        # cur.execute("SELECT * FROM foto")
        # real_id = cur.fetchall()
        # if real_id == []:
        #     max_id = 1
        # else:
        #     for row in real_id:
        #         max_id = int(row[0]) + 1
        # print(max_id)
        #
        #
        #
        # empPhoto = convertToBinaryData(file_path)
        #
        # # Convert data into tuple format
        # data_tuple = (max_id, empPhoto)
        # cur.execute("INSERT INTO foto VALUES(%s,%s)",data_tuple)
        # con.commit()
        # print("Image and file inserted successfully as a BLOB into a table")
        cur.close()

except Error as e:
    print(e)


work_time = (time.process_time() - start)
print(f"Время выполнения {work_time}")



if __name__ == '__main__':
    print("start")
