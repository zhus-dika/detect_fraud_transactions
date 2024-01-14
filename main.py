import psycopg2
from datetime import datetime
import py_scripts.read_data as read
import py_scripts.update_st_tables as update_tables
from config import DB_USERNAME, DB_PASSWORD, DB_PORT, DB_USER, DB_HOST

# Создание подключения к PostgreSQL
conn = psycopg2.connect(database = DB_USERNAME,
                        host =     DB_HOST,
                        user =     DB_USER,
                        password = DB_PASSWORD,
                        port =     DB_PORT)

# Отключение автокоммита
conn.autocommit = False

# Создание курсора
cursor = conn.cursor()

now = datetime.now()
today = now.strftime("%Y-%m-%d")
today = '2021-03-01'

df_terminals = read.terminals(today)

df_transactions = read.transactions(today)

df_blacklist = read.passport_blacklist(today)

update_tables.clean(cursor)

update_tables.update(cursor, df_terminals, df_blacklist, df_transactions)

# conn.commit()
# Закрываем соединение
cursor.close()
conn.close()