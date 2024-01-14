#  Записываем данные в отчет
import pandas as pd


def make(cursor, fraudulent_transactions):
    df_report = pd.DataFrame.from_dict(fraudulent_transactions)
    cursor.executemany(""" INSERT INTO dika_rep_fraud(
                              event_dt,
                              passport,
                              fio,
                              phone,
                              event_type,
                              report_dt
                              )
                            VALUES(to_timestamp(%s, 'yyyy-mm-dd hh24:mi:ss'), %s, %s, %s, %s, %s) """, df_report.values.tolist())