### Заполняем таблицы DWH_FACT
def fill(cursor):
    cursor.execute(""" INSERT INTO dika_dwh_fact_transactions(
                                trans_id,
                                trans_date,
                                amt,
                                card_num,
                                oper_type,
                                oper_result,
                                terminal
                              )
                            select
                                trans_id,
                                trans_date,
                                amt,
                                card_num,
                                oper_type,
                                oper_result,
                                terminal
                            from dika_stg_transactions""")

    cursor.execute(""" INSERT INTO dika_dwh_fact_passport_blacklist(
                              entry_dt,
                              passport_num
                              )
                            select
                              entry_dt,
                              passport_num
                            from dika_stg_passport_blacklist""")