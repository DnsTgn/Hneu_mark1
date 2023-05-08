import psycopg2
import logging
cur = None
con = None
def get_connect():
    logging.debug("Called <get_connect>)")
    try:
        conn = psycopg2.connect(
            database="mydb",
            user="postgres",
            password="Ng32fl3jdfqa",
            host="db",
            port="5432"
        )
        curr = conn.cursor()
        logging.info("DB connected!")
        print("[INFO] - БД під'єднана успішно")
        return [curr, conn]
    except:
        print("[WARN] - Невдала спроба під'єднатися до БД")
        logging.critical("DB is not connected!")


def add_id(value):
    try:
        cur.execute(f"INSERT INTO users (user_id) VALUES ({value}) ON CONFLICT (user_id) DO NOTHING;")
        con.commit()
        print("[INFO] - Додано ID : ", value)
        logging.info(f"id:{value} was added or already was")
    except:
        logging.error(f"id{value} was not added due to an error")
        print('[WARN] - ID не було додано до БД')



def add_add_subj(value,key):
    try:
        cur.execute(f"UPDATE users SET additional_subj_name = '{value}' WHERE user_id = {key};")
        con.commit()
        print(f"[INFO] - Додатковий предмет {value} був доданий для користувача з ID : {key}")
        logging.info(f"for id:{key} was added additional_subj_name = {value}")
    except:
        logging.error(f"for id{key} wasn`t added additional_subj_name")
        print(f"[WARN] - Додатковий предмет {value} НЕ був доданий для користувача з ID : {key}!")

def add_mark(subj,value,key):
    try:
        cur.execute(f"UPDATE users SET {subj} = {value} WHERE user_id = {key};")
        con.commit()
        print(f"[INFO] - Оцінка з {subj} - {value} була додана для користувача з ID : {key}")
        logging.info(f"for id:{key} was added mark = {value},subj = {subj}")
    except:
        logging.error(f"for id{key} wasn`t added mark{value}, subj = {subj}")
        print(f"[WARN] - Оцінка з {subj} - {value} НЕ була додана для користувача з ID : {key}!")
def add_spec_amount(spec):
    try:
        cur.execute(f"UPDATE spec_list SET amount = amount + 1 WHERE spec_code='{spec}';")
        con.commit()
        print(f"[INFO] - до спеціальності {spec} було додано 1 ")
        logging.info(f"for spec:{spec} was added 1")
    except:
        logging.warn(f"for spec:{spec} wasn`t added 1")
        print(f"[WARN] - до спеціальності {spec} НЕ було додано 1")

def get_add_subj(key):
    try:
        cur.execute(f"SELECT additional_subj_name FROM users WHERE user_id = {key}")
        result = cur.fetchone()
        print(f"for ID:{key}, additional subject is {result[0]}")
        logging.info(f"for id:{id} additional_subj_name was recieved")
        return result[0]
    except:
        logging.error(f"for id:{id} no additional_subj_name was recieved")

def get_all_info(key):
    try:
        cur.execute(f"SELECT * FROM users WHERE user_id = {key}")
        result = cur.fetchone()
        print(f"for ID:{key}, all info is {result}")
        logging.info(f"for id:{id} info was recieved")
        return list(result)
    except:
        logging.error(f"for id:{id} no info was recieved")

def get_users():
    try:
        cur.execute(f"SELECT user_id FROM users WHERE 1=1")
        results = cur.fetchall()
        column_values = [result[0] for result in results]
        print(column_values)
        logging.info('all users was recieved')
        return list(column_values)
    except:
        logging.error("no users was recieved")
def get_users_amount():
    try:
        cur.execute(f"SELECT count(user_id) FROM users WHERE 1=1")
        result = cur.fetchone()
        print(f"В базі є {result[0]} користувачів")
        logging.info("users amount was recieved")
        return result[0]
    except:
        logging.info("users amount wasn`t recieved")


def get_stats():
    try:
        cur.execute(f"SELECT * FROM spec_list ORDER BY amount DESC;")
        res = cur.fetchall()
        result = []
        for r in res:
            result.append([r[0],r[1]])
        logging.info("stats was recieved")
        return result
    except:
        logging.error("stats wasn`t recieved")