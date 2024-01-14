import psycopg2
from datetime import datetime
from py_scripts import read_data as read
from py_scripts import update_st_tables as update_tables
from config import DB_USERNAME, DB_PASSWORD, DB_PORT, DB_USER, DB_HOST
from py_scripts import dwh_fact

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
#************************
today = '2021-03-01'

#read data from files
df_terminals = read.terminals(today)

df_transactions = read.transactions(today)

df_blacklist = read.passport_blacklist(today)

#clean stage tables
update_tables.clean(cursor)

#update stage tables
update_tables.update(cursor, df_terminals, df_blacklist, df_transactions)

# fill data to DWH_FACT tables
dwh_fact.fill(cursor)
# conn.commit()
# Закрываем соединение
cursor.close()
conn.close()