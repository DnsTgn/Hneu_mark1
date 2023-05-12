import psycopg2
import logging
import os
class database:

    cur = None
    con = None

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance
    def __init__(self):
        if not self.cur and not self.con:
            self.cur, self.con = self.get_connect()
    def get_connect(self):
        logging.debug("Called <get_connect>)")
        try:
            conn = psycopg2.connect(
                database=os.environ.get("DB"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host=os.environ.get("DB_HOST"),
                port=os.environ.get("DB_PORT")
            )
            curr = conn.cursor()
            logging.info("DB connected!")
            print("[INFO] - БД під'єднана успішно")
            return [curr, conn]
        except:
            print("[WARN] - Невдала спроба під'єднатися до БД")
            logging.critical("DB is not connected!")


    def add_id(self,value):
        try:
            self.cur.execute(f"INSERT INTO users (user_id) VALUES ({value}) ON CONFLICT (user_id) DO NOTHING;")
            self.con.commit()
            print("[INFO] - Додано ID : ", value)
            logging.info(f"id:{value} was added or already was")
        except:
            logging.error(f"id{value} was not added due to an error")
            print('[WARN] - ID не було додано до БД')



    def add_add_subj(self,value,key):
        try:
            self.cur.execute(f"UPDATE users SET additional_subj_name = '{value}' WHERE user_id = {key};")
            self.con.commit()
            print(f"[INFO] - Додатковий предмет {value} був доданий для користувача з ID : {key}")
            logging.info(f"for id:{key} was added additional_subj_name = {value}")
        except:
            logging.error(f"for id{key} wasn`t added additional_subj_name")
            print(f"[WARN] - Додатковий предмет {value} НЕ був доданий для користувача з ID : {key}!")

    def add_mark(self,subj,value,key):
        try:
            self.cur.execute(f"UPDATE users SET {subj} = {value} WHERE user_id = {key};")
            self.con.commit()
            print(f"[INFO] - Оцінка з {subj} - {value} була додана для користувача з ID : {key}")
            logging.info(f"for id:{key} was added mark = {value},subj = {subj}")
        except:
            logging.error(f"for id{key} wasn`t added mark{value}, subj = {subj}")
            print(f"[WARN] - Оцінка з {subj} - {value} НЕ була додана для користувача з ID : {key}!")
    def add_spec_amount(self,spec):
        try:
            self.cur.execute(f"UPDATE spec_list SET amount = amount + 1 WHERE spec_code='{spec}';")
            self.con.commit()
            print(f"[INFO] - до спеціальності {spec} було додано 1 ")
            logging.info(f"for spec:{spec} was added 1")
        except:
            logging.warn(f"for spec:{spec} wasn`t added 1")
            print(f"[WARN] - до спеціальності {spec} НЕ було додано 1")

    def get_add_subj(self,key):
        try:
            self.cur.execute(f"SELECT additional_subj_name FROM users WHERE user_id = {key}")
            result = self.cur.fetchone()
            print(f"for ID:{key}, additional subject is {result[0]}")
            logging.info(f"for id:{id} additional_subj_name was recieved")
            return result[0]
        except:
            logging.error(f"for id:{id} no additional_subj_name was recieved")

    def get_all_info(self,key):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE user_id = {key}")
            result = self.cur.fetchone()
            print(f"for ID:{key}, all info is {result}")
            logging.info(f"for id:{id} info was recieved")
            return list(result)
        except:
            logging.error(f"for id:{id} no info was recieved")

    def get_users(self):
        try:
            self.cur.execute(f"SELECT user_id FROM users WHERE 1=1")
            results = self.cur.fetchall()
            column_values = [result[0] for result in results]
            print(column_values)
            logging.info('all users was recieved')
            return list(column_values)
        except:
            logging.error("no users was recieved")
    def get_users_amount(self):
        try:
            self.cur.execute(f"SELECT count(user_id) FROM users WHERE 1=1")
            result = self.cur.fetchone()
            print(f"В базі є {result[0]} користувачів")
            logging.info("users amount was recieved")
            return result[0]
        except:
            logging.info("users amount wasn`t recieved")


    def get_stats(self):
        try:
            self.cur.execute(f"SELECT * FROM spec_list ORDER BY amount DESC;")
            res = self.cur.fetchall()
            result = []
            for r in res:
                result.append([r[0],r[1]])
            logging.info("stats was recieved")
            return result
        except:
            logging.error("stats wasn`t recieved")