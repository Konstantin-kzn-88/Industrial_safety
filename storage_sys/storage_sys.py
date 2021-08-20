import sqlite3 as sq

def create_all_tabble():
    create_company_table()
    create_opo_table()
    create_documentation_table()


def create_documentation_table():
    """
    Создание третьей таблицы "Документация".
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS documentation")  # will delete the table if it exists

        # CREATE
        cur.execute("""CREATE TABLE IF NOT  EXISTS documentation (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            opo_id INTEGER NOT NULL,
            type_doc TEXT NOT NULL,
            reg_doc TEXT NOT NULL,
            date_doc YEAR NOT NULL   
            doc BLOB NOT NULL  
            )""")

def create_opo_table():
    """
    Создание второй таблицы "ОПО" - опасные производственные объекты.
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS opo")  # will delete the table if it exists

        # CREATE
        cur.execute("""CREATE TABLE IF NOT  EXISTS opo (
            opo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            name_opo TEXT NOT NULL,
            address_opo TEXT NOT NULL,
            reg_number_opo TEXT NOT NULL,
            class_opo TEXT NOT NULL
            )""")

def create_company_table():
    """
    Создание первой таблицы "Компания".
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS company")  # will delete the table if it exists

        # CREATE
        cur.execute("""CREATE TABLE IF NOT  EXISTS company (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_company TEXT NOT NULL,
            full_name_manager TEXT NOT NULL,
            ur_address TEXT NOT NULL,
            post_address TEXT NOT NULL,
            telephone DECIMAL NOT NULL,
            fax TEXT DECIMAL NULL,
            inn_number INT NOT NULL,
            kpp_number INT NOT NULL,
            ogrn_number INT NOT NULL,
            license_opo BLOB NOT NULL,
            reg_opo BLOB NOT NULL,
            position_pk BLOB NOT NULL,     
            position_crash BLOB NOT NULL  
            )""")

if __name__ == '__main__':
    create_all_tabble()
