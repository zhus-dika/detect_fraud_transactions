# read from terminals_.xlsx
import os
import shutil
import pandas as pd


def terminals(today):
    today_in_file = today[-2:] + today[-5:-3] + today[:4]

    df_terminals = pd.read_excel(open('data/terminals_' + today_in_file + '.xlsx', 'rb'), sheet_name='terminals')
    df_terminals['update_dt'] = today

    source = 'data/terminals_' + today_in_file + '.xlsx'
    target = 'archive/terminals_' + today_in_file + '.xlsx.backup'

    shutil.copyfile(source, target)

    if os.path.exists('data/terminals_' + today_in_file + '.xlsx'):
        os.remove('data/terminals_' + today_in_file + '.xlsx')
    return df_terminals

# read from passport_blacklist_.xlsx
def passport_blacklist(today):
    today_in_file = today[-2:] + today[-5:-3] + today[:4]
    df_blacklist = pd.read_excel(open('data/passport_blacklist_' + today_in_file + '.xlsx', 'rb'), sheet_name='blacklist')
    df_blacklist = df_blacklist.rename(columns={"date": "entry_dt", "passport": "passport_num"})

    source = 'data/passport_blacklist_' + today_in_file + '.xlsx'
    target = 'archive/passport_blacklist_' + today_in_file + '.xlsx.backup'

    shutil.copyfile(source, target)

    if os.path.exists('data/passport_blacklist_' + today_in_file + '.xlsx'):
        os.remove('data/passport_blacklist_' + today_in_file + '.xlsx')

    return df_blacklist

# read from transactions_.txt
def transactions(today):
    today_in_file = today[-2:] + today[-5:-3] + today[:4]
    df_transactions = pd.read_csv(open('data/transactions_' + today_in_file + '.txt', 'rb'), sep=';')
    df_transactions = df_transactions.rename(
        columns={'transaction_id': 'trans_id', 'transaction_date': 'trans_date', 'amount': 'amt'})
    df_transactions['amt'] = df_transactions['amt'].replace(',', '.', regex=True)
    df_transactions = df_transactions.astype({"amt": float})

    source = 'data/transactions_' + today_in_file + '.txt'
    target = 'archive/transactions_' + today_in_file + '.txt.backup'

    shutil.copyfile(source, target)

    if os.path.exists('data/transactions_' + today_in_file + '.txt'):
        os.remove('data/transactions_' + today_in_file + '.txt')
    return df_transactions