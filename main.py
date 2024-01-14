import psycopg2
from datetime import datetime
from py_scripts import read_data as read
from py_scripts import update_st_tables as update_tables
from py_scripts import dwh_fact, dwh_dim_hist, st_tables, fraud_operations
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
# conn.commit()
# fill data to DWH_FACT tables
dwh_fact.fill(cursor)

# fill data to DWH_DIM_HIST tables
dwh_dim_hist.insert(cursor)

dwh_dim_hist.update(cursor)

dwh_dim_hist.find_del(cursor)

dwh_dim_hist.add_deletions(cursor, today)

#get data from stage tables
df_clients = st_tables.clients(cursor)

df_cards= st_tables.cards(cursor)

df_accounts = st_tables.accounts(cursor)

# Выявим мошеннические операции
df_trans_cards_accounts_clients_terminals = fraud_operations.prepare_working_df(df_transactions, df_cards, df_accounts, df_clients, df_terminals)

#find 1st and 2d types fraud transactions
fraudulent_transactions = fraud_operations.detect12types(df_trans_cards_accounts_clients_terminals, df_blacklist, today)

#find 3d and 4th types fraud transactions
fraudulent_transactions = fraud_operations.detect34types(df_trans_cards_accounts_clients_terminals, fraudulent_transactions, today)
# conn.commit()
# Закрываем соединение
cursor.close()
conn.close()