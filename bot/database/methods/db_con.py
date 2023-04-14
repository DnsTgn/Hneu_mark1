import psycopg2

cur = None
con = None
def get_connect():
    try:
        conn = psycopg2.connect(
            database="HNEUmarkCalc",
            user="postgres",
            password="hneumarkcalc",
            host="localhost",
            port="5432"
        )
        curr = conn.cursor()
        print("[INFO] - БД під'єднана успішно")
    except:
        print("[WARN] - Невдала спроба під'єднатися до БД")
    return [curr,conn]

def add_id(value):
    try:
        cur.execute(f"INSERT INTO users (user_id) VALUES ({value}) ON CONFLICT (user_id) DO NOTHING;")
        con.commit()
        print("[INFO] - Додано ID : ", value)
    except:
        print('[WARN] - ID не було додано до БД')


def status_false(value):
    try:
        cur.execute(f"UPDATE users SET status = false WHERE user_id = {value};")
        con.commit()
        print("[INFO] - Було оновлено status на false для  ID : ", value)
    except:
        print('[WARN] - Помилка під час виконання запиту БД')
def status_true(value):
    try:
        cur.execute(f"UPDATE users SET status = true WHERE user_id = {value};")
        con.commit()
        print("[INFO] - Було оновлено status на true для  ID : ", value)
    except:
        print('[WARN] - Помилка під час виконання запиту БД')

def add_add_subj(value,key):
    try:
        cur.execute(f"UPDATE users SET additional_subj_name = '{value}' WHERE user_id = {key};")
        con.commit()
        print(f"[INFO] - Додатковий предмет {value} був доданий для користувача з ID : {key}")
    except:
        print(f"[WARN] - Додатковий предмет {value} НЕ був доданий для користувача з ID : {key}!")

def add_mark(subj,value,key):
    try:
        cur.execute(f"UPDATE users SET {subj} = {value} WHERE user_id = {key};")
        con.commit()
        print(f"[INFO] - Оцінка з {subj} - {value} була додана для користувача з ID : {key}")
    except:
        print(f"[WARN] - Оцінка з {subj} - {value} НЕ була додана для користувача з ID : {key}!")


def get_add_subj(key):
    cur.execute(f"SELECT additional_subj_name FROM users WHERE user_id = {key}")
    result = cur.fetchone()
    print(f"for ID:{key}, additional subject is {result[0]}")
    return result[0]

def get_all_info(key):
    cur.execute(f"SELECT * FROM users WHERE user_id = {key}")
    result = cur.fetchone()
    print(f"for ID:{key}, all info is {result}")
    return list(result)