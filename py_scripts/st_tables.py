import pandas as pd

# Датафрейм для clients
# Выполнение SQL кода в базе данных с возвратом результата
def clients(cursor):
    cursor.execute( "select * from dika_stg_clients" )
    records = cursor.fetchall()
    # Формирование DataFrame
    names = [ x[0] for x in cursor.description ]
    df_clients = pd.DataFrame( records, columns = names )
    return df_clients

# Датафрейм для cards
# Выполнение SQL кода в базе данных с возвратом результата
def cards(cursor):
    cursor.execute( "select * from dika_stg_cards" )
    records = cursor.fetchall()
    # Формирование DataFrame
    names = [ x[0] for x in cursor.description ]
    df_cards = pd.DataFrame( records, columns = names )
    return df_cards

# Датафрейм для accounts
# Выполнение SQL кода в базе данных с возвратом результата
def accounts(cursor):
    cursor.execute( "select * from dika_stg_accounts" )
    records = cursor.fetchall()
    # Формирование DataFrame
    names = [ x[0] for x in cursor.description ]
    df_accounts = pd.DataFrame( records, columns = names )
    return df_accounts