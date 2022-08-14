import psycopg2


# Функция, создающая структуру БД (таблицы)
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS clients(
                    client_id SERIAL PRIMARY KEY,
                    fname VARCHAR NOT NULL,
                    lname VARCHAR NOT NULL,
                    email VARCHAR NOT NULL);""")
        cur.execute("""CREATE TABLE IF NOT EXISTS phones(
                    phone_id SERIAL PRIMARY KEY,
                    client_id INT NOT NULL REFERENCES clients(client_id),
                    number VARCHAR NOT NULL);""")

        conn.commit()  # фиксируем в БД


# Функция, позволяющая добавить нового клиента
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO clients(fname, lname, email) 
                    VALUES(%s, %s, %s) RETURNING client_id;""",  # returning возвращает id клиента
                    (first_name, last_name, email))

        if phones:
            cur.execute("""INSERT INTO phones(client_id, number) 
                        VALUES(%s, %s);""",
                        (cur.fetchone(), phones))   # fetchone принимает id клиента

        conn.commit()  # фиксируем в БД


# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phones(client_id, number) 
                    VALUES(%s, %s);""",
                    (client_id, phone))

        conn.commit()  # фиксируем в БД


# Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("""UPDATE clients SET fname=%s WHERE client_id=%s;""",
                        (first_name, client_id))

        if last_name:
            cur.execute("""UPDATE clients SET lname=%s WHERE client_id=%s;""",
                        (last_name, client_id))

        if email:
            cur.execute("""UPDATE clients SET email=%s WHERE client_id=%s;""",
                        (email, client_id))

        if phones:
            cur.execute("""UPDATE phones SET number=%s WHERE client_id=%s;""",
                        (phones, client_id))

        conn.commit()  # фиксируем в БД


# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id, phone_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE phone_id=%s AND client_id=%s;""",
                    (phone_id, client_id))

        conn.commit()  # фиксируем в БД


# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE client_id=%s;""",
                    (client_id))

        cur.execute("""DELETE FROM clients WHERE client_id=%s;""",
                    (client_id))

        conn.commit()  # фиксируем в БД


# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("""SELECT fname, lname, email, p.number FROM clients c
                        JOIN phones p ON p.client_id = c.client_id
                        WHERE fname=%s;""",
                        (first_name,))

        if last_name:
            cur.execute("""SELECT fname, lname, email, p.number FROM clients c
                        JOIN phones p ON p.client_id = c.client_id
                        WHERE lname=%s;""",
                        (last_name,))

        if email:
            cur.execute("""SELECT fname, lname, email, p.number FROM clients c
                        JOIN phones p ON p.client_id = c.client_id
                        WHERE email=%s;""",
                        (email,))

        if phone:
            cur.execute("""SELECT c.fname, c.lname, c.email, p.number FROM phones p
                        JOIN clients c ON p.client_id = c.client_id
                        WHERE number=%s;""",
                        (phone,))

        print(cur.fetchone())
        conn.commit()  # фиксируем в БД


with psycopg2.connect(database="HW9", user="postgres", password="********") as conn:
    create_db(conn)
    add_client(conn, 'ivan', 'popov', 'ivanpopov@gmail.com', 71234567890)
    add_phone(conn, 1, 98765432100)
    change_client(conn, 1, 'Dima', 'Ivanov', 'dimaivanov@gmail.com', 1234567890)
    delete_phone(conn, 1, 2)
    delete_client(conn, '1')
    find_client(conn, 'ivan')
    find_client(conn, last_name='popov')
    find_client(conn, email='ivanpopov@gmail.com')
    find_client(conn, phone='71234567890')
conn.close()