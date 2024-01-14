# Заполняем таблицы DWH_DIM_..._HIST
# Добавляем вставки в таблицах
def insert(cursor):
    cursor.execute(""" insert into dika_dwh_dim_cards_hist( card_num, account, effective_from, effective_to, deleted_flg )
                        select 
                            stg.card_num, 
                            stg.account, 
                            stg.create_dt, 
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_cards stg
                        left join dika_dwh_dim_cards_hist tgt
                        on stg.card_num = tgt.card_num
                        where tgt.card_num is null""")

    cursor.execute(""" insert into dika_dwh_dim_clients_hist( 
                            client_id, 
                            last_name, 
                            first_name, 
                            patronymic, 
                            date_of_birth, 
                            passport_num, 
                            passport_valid_to, 
                            phone, 
                            effective_from, 
                            effective_to, 
                            deleted_flg )
                        select 
                            stg.client_id, 
                            stg.last_name, 
                            stg.first_name, 
                            stg.patronymic, 
                            stg.date_of_birth, 
                            stg.passport_num, 
                            stg.passport_valid_to, 
                            stg.phone, 
                            stg.create_dt, 
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_clients stg
                        left join dika_dwh_dim_clients_hist tgt
                        on stg.client_id = tgt.client_id
                        where tgt.client_id is null""")

    cursor.execute(""" insert into dika_dwh_dim_accounts_hist( account, valid_to, client, effective_from, effective_to, deleted_flg )
                        select 
                            stg.account, 
                            stg.valid_to,
                            stg.client, 
                            stg.create_dt, 
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_accounts stg
                        left join dika_dwh_dim_accounts_hist tgt
                        on stg.account = tgt.account
                        where tgt.account is null""")

    cursor.execute(""" insert into dika_dwh_dim_terminals_hist(
                        terminal_id,
                        terminal_type,
                        terminal_city,
                        terminal_address,
                        effective_from, 
                        effective_to, 
                        deleted_flg )
                        select 
                            stg.terminal_id, 
                            stg.terminal_type,
                            stg.terminal_city,
                            stg.terminal_address,
                            stg.update_dt, 
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_terminals stg
                        left join dika_dwh_dim_terminals_hist tgt
                        on stg.terminal_id = tgt.terminal_id
                        where tgt.terminal_id is null""")

# Обновляем данные
def update(cursor):
    cursor.execute(""" update dika_dwh_dim_cards_hist
                        set 
                            effective_to = tmp.update_dt - interval '1 day'
                        from (
                            select 
                                stg.card_num, 
                                stg.account, 
                                stg.update_dt
                            from dika_stg_cards stg
                            inner join dika_dwh_dim_cards_hist tgt
                            on stg.card_num = tgt.card_num
                            where stg.account <> tgt.account 
                             or ( stg.account is null and tgt.account is not null ) 
                             or ( stg.account is not null and tgt.account is null )
                        ) tmp
                        where dika_dwh_dim_cards_hist.card_num = tmp.card_num""")
    cursor.execute(""" insert into dika_dwh_dim_cards_hist( card_num, account, effective_from, effective_to, deleted_flg )
                        select 
                            stg.card_num, 
                            stg.account, 
                            stg.update_dt,
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_cards stg
                        left join dika_dwh_dim_cards_hist tgt
                        on stg.card_num = tgt.card_num
                        where tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')""")

    cursor.execute(""" update dika_dwh_dim_clients_hist
                        set 
                            effective_to = tmp.update_dt - interval '1 day'
                        from (
                            select 
                                stg.client_id, 
                                stg.last_name, 
                                stg.first_name,
                                stg.patronymic,
                                stg.date_of_birth,
                                stg.passport_num,
                                stg.passport_valid_to,
                                stg.phone,
                                stg.update_dt
                            from dika_stg_clients stg
                            inner join dika_dwh_dim_clients_hist tgt
                            on stg.client_id = tgt.client_id
                            where 
                             stg.last_name <> tgt.last_name 
                             or ( stg.last_name is null and tgt.last_name is not null ) 
                             or ( stg.last_name is not null and tgt.last_name is null )
                             or stg.first_name <> tgt.first_name 
                             or ( stg.first_name is null and tgt.first_name is not null ) 
                             or ( stg.first_name is not null and tgt.first_name is null )
                             or stg.patronymic <> tgt.patronymic 
                             or ( stg.patronymic is null and tgt.patronymic is not null ) 
                             or ( stg.patronymic is not null and tgt.patronymic is null )
                             or stg.date_of_birth <> tgt.date_of_birth 
                             or ( stg.date_of_birth is null and tgt.date_of_birth is not null ) 
                             or ( stg.date_of_birth is not null and tgt.date_of_birth is null )
                             or stg.passport_num <> tgt.passport_num 
                             or ( stg.passport_num is null and tgt.passport_num is not null ) 
                             or ( stg.passport_num is not null and tgt.passport_num is null )
                             or stg.passport_valid_to <> tgt.passport_valid_to 
                             or ( stg.passport_valid_to is null and tgt.passport_valid_to is not null ) 
                             or ( stg.passport_valid_to is not null and tgt.passport_valid_to is null )
                             or stg.phone <> tgt.phone 
                             or ( stg.phone is null and tgt.phone is not null ) 
                             or ( stg.phone is not null and tgt.phone is null )
                        ) tmp
                        where dika_dwh_dim_clients_hist.client_id = tmp.client_id""")
    cursor.execute(""" insert into dika_dwh_dim_clients_hist( client_id, 
                                                            last_name, 
                                                            first_name, 
                                                            patronymic, 
                                                            date_of_birth, 
                                                            passport_num, 
                                                            passport_valid_to,
                                                            phone,
                                                            effective_from, 
                                                            effective_to, 
                                                            deleted_flg )
                        select 
                            stg.client_id, 
                            stg.last_name, 
                            stg.first_name,
                            stg.patronymic,
                            stg.date_of_birth,
                            stg.passport_num,
                            stg.passport_valid_to,
                            stg.phone,
                            stg.update_dt,
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_clients stg
                        left join dika_dwh_dim_clients_hist tgt
                        on stg.client_id = tgt.client_id
                        where tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')""")

    cursor.execute(""" update dika_dwh_dim_accounts_hist
                        set 
                            effective_to = tmp.update_dt - interval '1 day'
                        from (
                            select 
                                stg.account, 
                                stg.valid_to, 
                                stg.client,
                                stg.update_dt
                            from dika_stg_accounts stg
                            inner join dika_dwh_dim_accounts_hist tgt
                            on stg.account = tgt.account
                            where stg.client <> tgt.client 
                             or ( stg.client is null and tgt.client is not null ) 
                             or ( stg.client is not null and tgt.client is null )
                             or stg.valid_to <> tgt.valid_to 
                             or ( stg.valid_to is null and tgt.valid_to is not null ) 
                             or ( stg.valid_to is not null and tgt.valid_to is null )
                        ) tmp
                        where dika_dwh_dim_accounts_hist.account = tmp.account""")
    cursor.execute(""" insert into dika_dwh_dim_accounts_hist( account, valid_to, client, effective_from, effective_to, deleted_flg )
                        select 
                            stg.account, 
                            stg.valid_to,
                            stg.client,
                            stg.update_dt,
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_accounts stg
                        left join dika_dwh_dim_accounts_hist tgt
                        on stg.account = tgt.account
                        where tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')""")

    cursor.execute(""" update dika_dwh_dim_terminals_hist
                        set 
                            effective_to = tmp.update_dt - interval '1 day'
                        from (
                            select 
                                stg.terminal_id, 
                                stg.terminal_type, 
                                stg.terminal_city,
                                stg.terminal_address,
                                stg.update_dt
                            from dika_stg_terminals stg
                            inner join dika_dwh_dim_terminals_hist tgt
                            on stg.terminal_id = tgt.terminal_id
                            where stg.terminal_type <> tgt.terminal_type 
                             or ( stg.terminal_type is null and tgt.terminal_type is not null ) 
                             or ( stg.terminal_type is not null and tgt.terminal_type is null )
                             or stg.terminal_city <> tgt.terminal_city 
                             or ( stg.terminal_city is null and tgt.terminal_city is not null ) 
                             or ( stg.terminal_city is not null and tgt.terminal_city is null )
                             or stg.terminal_address <> tgt.terminal_address 
                             or ( stg.terminal_address is null and tgt.terminal_address is not null ) 
                             or ( stg.terminal_address is not null and tgt.terminal_address is null )
                        ) tmp
                        where dika_dwh_dim_terminals_hist.terminal_id = tmp.terminal_id""")
    cursor.execute(""" insert into dika_dwh_dim_terminals_hist( terminal_id, terminal_type, terminal_city, terminal_address, effective_from, effective_to, deleted_flg )
                        select 
                            stg.terminal_id, 
                            stg.terminal_type, 
                            stg.terminal_city,
                            stg.terminal_address,
                            stg.update_dt,
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            false
                        from dika_stg_terminals stg
                        left join dika_dwh_dim_terminals_hist tgt
                        on stg.terminal_id = tgt.terminal_id
                        where tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')""")

# Добавляем айдишники для определения удаленных
def find_del(cursor):
    cursor.execute(""" insert into dika_stg_cards_del( card_num )
                            select card_num from dika_stg_cards""")

    cursor.execute(""" insert into dika_stg_clients_del( client_id )
                            select client_id from dika_stg_clients""")

    cursor.execute(""" insert into dika_stg_accounts_del( account )
                            select account from dika_stg_accounts""")

    cursor.execute(""" insert into dika_stg_terminals_del( terminal_id )
                        select terminal_id from dika_stg_terminals""")

# Формируем историю удалений в таблицах DWH_DIM_..._HIST
# dika_dwh_dim_cards_hist
def add_deletions(cursor, today):
    cursor.execute("""update dika_dwh_dim_cards_hist
                      set
                        effective_to = to_date(%s, 'YYYY-MM-DD') - interval '1 day'
                      from (
                        select
                          tgt.card_num
                        from dika_dwh_dim_cards_hist tgt
                        left join dika_stg_cards_del stg
                        on stg.card_num = tgt.card_num
                        where stg.card_num is null
                      ) tmp
                      where dika_dwh_dim_cards_hist.card_num = tmp.card_num and dika_dwh_dim_cards_hist.effective_to=to_date('2999-12-31', 'YYYY-MM-DD')""",
                   (today,))

    cursor.execute(""" insert into dika_dwh_dim_cards_hist( card_num, account, effective_from, effective_to, deleted_flg )
                          select
                            tmp.card_num,
                            tmp.account,
                            to_date(%s, 'YYYY-MM-DD'),
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            true
                          from (
                            select
                              tgt.card_num,
                              tgt.account
                            from dika_dwh_dim_cards_hist tgt
                            left join dika_stg_cards_del stg
                            on stg.card_num = tgt.card_num
                            where stg.card_num is null and tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')
                          ) tmp""", (today,))

    cursor.execute("""update dika_dwh_dim_accounts_hist
                      set
                        effective_to = to_date(%s, 'YYYY-MM-DD') - interval '1 day'
                      from (
                        select
                          tgt.account
                        from dika_dwh_dim_accounts_hist tgt
                        left join dika_stg_accounts_del stg
                        on stg.account = tgt.account
                        where stg.account is null
                      ) tmp
                      where dika_dwh_dim_accounts_hist.account = tmp.account and dika_dwh_dim_accounts_hist.effective_to=to_date('2999-12-31', 'YYYY-MM-DD')""",
                   (today,))

    cursor.execute(""" insert into dika_dwh_dim_accounts_hist( account, valid_to, client, effective_from, effective_to, deleted_flg )
                          select
                            tmp.account,
                            tmp.valid_to,
                            tmp.client,
                            to_date(%s, 'YYYY-MM-DD'),
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            true
                          from (
                            select
                              tgt.account,
                              tgt.valid_to,
                              tgt.client
                            from dika_dwh_dim_accounts_hist tgt
                            left join dika_stg_accounts_del stg
                            on stg.account = tgt.account
                            where stg.account is null and tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')
                          ) tmp""", (today,))

    cursor.execute("""update dika_dwh_dim_clients_hist
                      set
                        effective_to = to_date(%s, 'YYYY-MM-DD') - interval '1 day'
                      from (
                        select
                          tgt.client_id
                        from dika_dwh_dim_clients_hist tgt
                        left join dika_stg_clients_del stg
                        on stg.client_id = tgt.client_id
                        where stg.client_id is null
                      ) tmp
                      where dika_dwh_dim_clients_hist.client_id = tmp.client_id and dika_dwh_dim_clients_hist.effective_to=to_date('2999-12-31', 'YYYY-MM-DD')""",
                   (today,))

    cursor.execute(""" insert into dika_dwh_dim_clients_hist( client_id, 
                                                            last_name, 
                                                            first_name, 
                                                            patronymic, 
                                                            date_of_birth, 
                                                            passport_num,
                                                            passport_valid_to,
                                                            phone,
                                                            effective_from, 
                                                            effective_to, 
                                                            deleted_flg )
                          select
                            tmp.client_id,
                            tmp.last_name, 
                            tmp.first_name, 
                            tmp.patronymic, 
                            tmp.date_of_birth, 
                            tmp.passport_num,
                            tmp.passport_valid_to,
                            tmp.phone,
                            to_date(%s, 'YYYY-MM-DD'),
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            true
                          from (
                            select
                              tgt.client_id,
                              tgt.last_name, 
                              tgt.first_name, 
                              tgt.patronymic, 
                              tgt.date_of_birth, 
                              tgt.passport_num,
                              tgt.passport_valid_to,
                              tgt.phone
                            from dika_dwh_dim_clients_hist tgt
                            left join dika_stg_clients_del stg
                            on stg.client_id = tgt.client_id
                            where stg.client_id is null and tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')
                          ) tmp""", (today,))

    cursor.execute("""update dika_dwh_dim_terminals_hist
                      set
                        effective_to = to_date(%s, 'YYYY-MM-DD') - interval '1 day'
                      from (
                        select
                          tgt.terminal_id
                        from dika_dwh_dim_terminals_hist tgt
                        left join dika_stg_terminals_del stg
                        on stg.terminal_id = tgt.terminal_id
                        where stg.terminal_id is null
                      ) tmp
                      where dika_dwh_dim_terminals_hist.terminal_id = tmp.terminal_id and dika_dwh_dim_terminals_hist.effective_to=to_date('2999-12-31', 'YYYY-MM-DD')""",
                   (today,))

    cursor.execute(""" insert into dika_dwh_dim_terminals_hist( terminal_id, 
                                                            terminal_type, 
                                                            terminal_city,
                                                            terminal_address,
                                                            effective_from, 
                                                            effective_to, 
                                                            deleted_flg )
                          select
                            tmp.terminal_id,
                            tmp.terminal_type, 
                            tmp.terminal_city, 
                            tmp.terminal_address, 
                            to_date(%s, 'YYYY-MM-DD'),
                            to_date('2999-12-31', 'YYYY-MM-DD'),
                            true
                          from (
                            select
                              tgt.terminal_id,
                              tgt.terminal_type, 
                              tgt.terminal_city, 
                              tgt.terminal_address
                            from dika_dwh_dim_terminals_hist tgt
                            left join dika_stg_terminals_del stg
                            on stg.terminal_id = tgt.terminal_id
                            where stg.terminal_id is null and tgt.effective_to < to_date('2999-12-31', 'YYYY-MM-DD')
                          ) tmp""", (today,))