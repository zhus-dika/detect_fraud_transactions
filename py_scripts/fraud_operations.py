from datetime import datetime
import pandas as pd
from dateutil import parser


def prepare_working_df(df_transactions, df_cards, df_accounts, df_clients, df_terminals):
    df_trans_cards = pd.merge(df_transactions[['trans_id', 'trans_date', 'card_num', 'oper_result', 'terminal', 'amt']],
                              df_cards, on=['card_num'])

    df_trans_cards_accounts = pd.merge(df_trans_cards, df_accounts, on=['account'])

    df_trans_cards_accounts_clients = pd.merge(df_trans_cards_accounts.rename(columns={"client": "client_id"}), df_clients[
        ['client_id', 'last_name', 'first_name', 'patronymic', 'passport_num', 'passport_valid_to', 'phone']],
                                               on='client_id')
    df_trans_cards_accounts_clients_terminals = pd.merge(
        df_trans_cards_accounts_clients.rename(columns={"terminal": "terminal_id"}),
        df_terminals[['terminal_id', 'terminal_city']], on='terminal_id')
    return df_trans_cards_accounts_clients_terminals

###  1-го и 2-го типов
def detect12types(df_trans_cards_accounts_clients_terminals, df_blacklist, today):
    fraudulent_transactions = {'event_dt': [], 'passport': [], 'fio': [], 'phone': [], 'event_type': [], 'report_dt': []}
    for index, row in df_trans_cards_accounts_clients_terminals.iterrows():
        if row['oper_result'] == 'SUCCESS':

            if (row['passport_valid_to'] != None and parser.parse(str(row['passport_valid_to'])) <= parser.parse(today)) or \
                    row['passport_num'] in df_blacklist['passport_num'].values:
                fraudulent_transactions['event_dt'].append(str(row['trans_date']))
                fraudulent_transactions['passport'].append(row['passport_num'])
                fraudulent_transactions['fio'].append(row['last_name'] + ' ' + row['first_name'] + ' ' + row['patronymic'])
                fraudulent_transactions['phone'].append(row['phone'])
                fraudulent_transactions['event_type'].append(1)
                fraudulent_transactions['report_dt'].append(today)
            if parser.parse(str(row['valid_to'])) <= parser.parse(today):
                fraudulent_transactions['event_dt'].append(str(row['trans_date']))
                fraudulent_transactions['passport'].append(row['passport_num'])
                fraudulent_transactions['fio'].append(row['last_name'] + ' ' + row['first_name'] + ' ' + row['patronymic'])
                fraudulent_transactions['phone'].append(row['phone'])
                fraudulent_transactions['event_type'].append(2)
                fraudulent_transactions['report_dt'].append(today)
    return fraudulent_transactions

###  3-го и 4-го типов
def detect34types(df_trans_cards_accounts_clients_terminals, fraudulent_transactions, today):
    df_trans_cards_accounts_clients_terminals_grouped = df_trans_cards_accounts_clients_terminals.groupby("client_id")
    card_nums = df_trans_cards_accounts_clients_terminals_grouped.groups.keys()

    for idx in card_nums:
        df_group = pd.DataFrame(df_trans_cards_accounts_clients_terminals_grouped.get_group(idx)).sort_values(
            by=['trans_date'])
        cnt = 0
        cnt_reject = 0
        time_spent_sec = 0
        for index, row in df_group.iterrows():
            fmt = '%Y-%m-%d %H:%M:%S'
            row['trans_date'] = datetime.strptime(row['trans_date'], fmt)
            if cnt > 0:
                res = row['trans_date'] - row_prev['trans_date']
                # 3d type event
                if res.total_seconds() / 3600 < 1 and row['terminal_city'] != row_prev['terminal_city']:
                    if row['oper_result'] == 'SUCCESS' and row_prev['oper_result'] == 'SUCCESS':
                        fraudulent_transactions['event_dt'].append(str(row['trans_date']))
                        fraudulent_transactions['passport'].append(row['passport_num'])
                        fraudulent_transactions['fio'].append(
                            row['last_name'] + ' ' + row['first_name'] + ' ' + row['patronymic'])
                        fraudulent_transactions['phone'].append(row['phone'])
                        fraudulent_transactions['event_type'].append(3)
                        fraudulent_transactions['report_dt'].append(today)
                else:
                    if row['oper_result'] == 'REJECT' and row_prev['oper_result'] == 'REJECT' and float(row['amt']) < float(
                            row_prev['amt']):
                        cnt_reject += 1
                        time_spent_sec += res.total_seconds()
                    else:
                        # 4th type event
                        if cnt_reject >= 2 and time_spent_sec / 60 <= 20 and float(row['amt']) < float(row_prev['amt']):
                            fraudulent_transactions['event_dt'].append(str(row['trans_date']))
                            fraudulent_transactions['passport'].append(row['passport_num'])
                            fraudulent_transactions['fio'].append(
                                row['last_name'] + ' ' + row['first_name'] + ' ' + row['patronymic'])
                            fraudulent_transactions['phone'].append(row['phone'])
                            fraudulent_transactions['event_type'].append(4)
                            fraudulent_transactions['report_dt'].append(today)
                        time_spent_sec = 0
                        cnt_reject = 0
            row_prev = row
            cnt += 1
    return fraudulent_transactions