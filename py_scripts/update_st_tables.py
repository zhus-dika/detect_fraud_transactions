# Подготовка данных, очищаем стейджинговые таблицы
def clean(cursor):
    cursor.execute("truncate table dika_stg_transactions ")
    cursor.execute("truncate table dika_stg_terminals ")
    cursor.execute("truncate table dika_stg_passport_blacklist ")
    cursor.execute("truncate table dika_stg_cards ")
    cursor.execute("truncate table dika_stg_accounts ")
    cursor.execute("truncate table dika_stg_clients ")

### Заполняем актуальными данными стейджинговые таблицы из бд
# staging cards
def update(cursor, df_terminals, df_blacklist, df_transactions):
    cursor.execute(""" INSERT INTO dika_stg_cards(
                              card_num,
                              account,
                              create_dt,
                              update_dt
                              )
                            SELECT
                              card_num,
                              account,
                              create_dt,
                              update_dt
                            FROM info.cards""")
    # staging clients
    cursor.execute(""" INSERT INTO dika_stg_clients(
                              client_id,
                              last_name,
                              first_name,
                              patronymic,
                              date_of_birth,
                              passport_num,
                              passport_valid_to,
                              phone,
                              create_dt,
                              update_dt
                              )
                            select
                              client_id,
                              last_name,
                              first_name,
                              patronymic,
                              date_of_birth,
                              passport_num,
                              passport_valid_to,
                              phone,
                              create_dt,
                              update_dt
                            from info.clients""")

    # staging accounts
    cursor.execute(""" INSERT INTO dika_stg_accounts(
                              account,
                                valid_to,
                                client,
                              create_dt,
                              update_dt
                              )
                              select
                                account,
                                valid_to,
                                client,
                                create_dt,
                                update_dt
                              from info.accounts""")

    ### Заполняем актуальными данными стейджинговые таблицы из файлов
    # stg passport blacklist

    cursor.executemany(""" INSERT INTO dika_stg_passport_blacklist(
                              entry_dt,
                              passport_num
                              )
                            VALUES(%s, %s) """, df_blacklist.values.tolist())

    # stg terminals
    cursor.executemany(""" INSERT INTO dika_stg_terminals(
                              terminal_id,
                              terminal_type,
                                terminal_city,
                                terminal_address,
                              update_dt
                              )
                            VALUES(%s, %s, %s, %s, %s) """, df_terminals.values.tolist())

    # stg transactions
    cursor.executemany(""" INSERT INTO dika_stg_transactions(
                                trans_id,
                                trans_date,
                                amt,
                                card_num,
                                oper_type,
                                oper_result,
                                terminal
                              )
                            VALUES(%s, %s, %s, %s, %s, %s, %s) """, df_transactions.values.tolist())