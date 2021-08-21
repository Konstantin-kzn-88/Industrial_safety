import sqlite3 as sq

def create_all_tabble():
    create_company_table()
    create_opo_table()
    create_documentation_table()
    create_line_obj_table()
    create_state_obj_table()
    create_build_obj_table()
    create_project_table()


def create_project_table():
    """
    Создание седьмой таблицы "Проект".
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS project")  # will delete the table if it exists

        # CREATE
        cur.execute("""CREATE TABLE IF NOT  EXISTS project (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            opo_id INTEGER NOT NULL,
            line_obj_id INTEGER,
            state_obj_id INTEGER,
            build_obj_id INTEGER,
            name_project TEXT NOT NULL,
            date_project DATE NOT NULL, 
            pz_project BLOB NOT NULL,
            pzu_project BLOB NOT NULL,
            kr_project BLOB NOT NULL,
            ios_project BLOB NOT NULL,
            pos_project BLOB NOT NULL,
            another_project BLOB NOT NULL  
            )""")

def create_build_obj_table():
    """
    Создание шестой таблицы "Здания/сооружения".
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS build_obj")  # will delete the table if it exists

        # # CREATE
        # cur.execute("""CREATE TABLE IF NOT  EXISTS build_obj (
        #     build_obj_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     name_obj TEXT NOT NULL,
        #     status TEXT NOT NULL,
        #     date_manufacture DATE NOT NULL,
        #     date_entry DATE NOT NULL,
        #     date_upto DATE NOT NULL,
        #     opo_id INTEGER NOT NULL,
        #     FOREIGN KEY (opo) REFERENCES opo(opo_id));
        #     )""")

def create_state_obj_table():
    """
    Создание пятой таблицы "Стационарные объекты".
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS state_obj")  # will delete the table if it exists

        # CREATE
        cur.execute("""CREATE TABLE IF NOT  EXISTS state_obj (
            state_obj_id INTEGER PRIMARY KEY AUTOINCREMENT,
            opo_id INTEGER NOT NULL,
            reg_number INTEGER NOT NULL,
            name_obj TEXT NOT NULL,
            substance TEXT NOT NULL,
            volume INTEGER NOT NULL,
            temperature INTEGER NOT NULL,
            pressure INTEGER NOT NULL,
            alpha INTEGER NOT NULL,
            status TEXT NOT NULL,
            date_manufacture DATE NOT NULL,
            date_entry DATE NOT NULL,
            date_upto DATE NOT NULL,   
            passport BLOB NOT NULL  
            )""")

def create_line_obj_table():
    """
    Создание четвертой таблицы "Линейные объекты".
    Удаление производится для того что-бы не опасть на ошибку
    """
    with sq.connect("data.db") as con:
        cur = con.cursor()

        # DEL
        cur.execute("DROP TABLE IF EXISTS line_obj")  # will delete the table if it exists

        # CREATE
        cur.execute("""CREATE TABLE IF NOT  EXISTS line_obj (
            line_obj_id INTEGER PRIMARY KEY AUTOINCREMENT,
            opo_id INTEGER NOT NULL,
            reg_number INTEGER NOT NULL,
            name_obj TEXT NOT NULL,
            substance TEXT NOT NULL,
            lenght INTEGER NOT NULL,
            diameter INTEGER NOT NULL,
            pressure INTEGER NOT NULL,
            status TEXT NOT NULL,
            date_manufacture DATE NOT NULL,
            date_entry DATE NOT NULL,
            date_upto DATE NOT NULL,   
            passport BLOB NOT NULL  
            )""")

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
        cur.execute("""CREATE TABLE IF NOT EXISTS opo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            type_doc TEXT NOT NULL,
                            reg_doc TEXT NOT NULL,
                            date_doc DATE NOT NULL, 
                            doc BLOB NOT NULL,
                            id_opo INTEGER NOT NULL, 
                            FOREIGN KEY (id_opo) REFERENCES opo(id));
                    """)



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
        cur.execute("""CREATE TABLE IF NOT EXISTS opo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name_opo TEXT NOT NULL,
                            address_opo TEXT NOT NULL,
                            reg_number_opo TEXT NOT NULL,
                            class_opo TEXT NOT NULL,
                            id_company INTEGER NOT NULL, 
                            FOREIGN KEY (id_company) REFERENCES company(id));
                    """)


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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
