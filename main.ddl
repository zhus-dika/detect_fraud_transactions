create table dika_stg_transactions(
	trans_id varchar(20),
	trans_date timestamp(0),
	card_num varchar(20),
 	oper_type varchar(20),
 	amt decimal,
 	oper_result varchar(50),
 	terminal varchar(20)
);

create table dika_stg_terminals(
	terminal_id varchar(20),
	terminal_type varchar(20),
	terminal_city varchar(50),
	terminal_address varchar(50),
	update_dt timestamp(0)
);

create table dika_stg_terminals_del(
	terminal_id varchar(20)
);

create table dika_stg_passport_blacklist(
	passport_num varchar(15),
	entry_dt timestamp(0),
	update_dt timestamp(0)
);

create table dika_stg_cards(
	card_num varchar(20),
	account varchar(20),
	create_dt timestamp(0),
	update_dt timestamp(0)
);

create table dika_stg_cards_del(
	card_num varchar(20)
);

create table dika_stg_accounts(
	account varchar(20),
	valid_to date,
	client varchar(20),
	create_dt timestamp(0),
	update_dt timestamp(0)
);

create table dika_stg_accounts_del(
	account varchar(20)
);

create table dika_stg_clients(
	client_id varchar(10),
	last_name varchar(20),
	first_name varchar(20),
	patronymic varchar(20),
	date_of_birth date,
	passport_num varchar(15),
	passport_valid_to date,
	phone varchar(16),
	create_dt timestamp(0),
	update_dt timestamp(0)
);

create table dika_stg_clients_del(
	client_id varchar(10)
);


create table dika_dwh_fact_transactions(
	trans_id varchar(20),
	trans_date timestamp(0),
	card_num varchar(20),
 	oper_type varchar(20),
 	amt decimal,
 	oper_result varchar(50),
 	terminal varchar(20)
);

create table dika_dwh_fact_passport_blacklist(
	passport_num varchar(15),
	entry_dt date
);

create table dika_dwh_dim_terminals_hist(
	terminal_id varchar(20),
	terminal_type varchar(20),
	terminal_city varchar(50),
	terminal_address varchar(50),
	effective_from timestamp(0),
	effective_to timestamp(0),
	deleted_flg boolean
);

create table dika_dwh_dim_cards_hist(
	card_num varchar(20),
	account varchar(20),
	effective_from timestamp(0),
	effective_to timestamp(0),
	deleted_flg boolean
);

create table dika_dwh_dim_accounts_hist(
	account varchar(20),
	valid_to date,
	client varchar(20),
	effective_from timestamp(0),
	effective_to timestamp(0),
	deleted_flg boolean
);

create table dika_dwh_dim_clients_hist(
	client_id varchar(10),
	last_name varchar(20),
	first_name varchar(20),
	patronymic varchar(20),
	date_of_birth date,
	passport_num varchar(15),
	passport_valid_to date,
	phone varchar(16),
	effective_from timestamp(0),
	effective_to timestamp(0),
	deleted_flg boolean
);

create table dika_rep_fraud(
	event_dt timestamp(0),
	passport varchar(15),
	fio varchar(50),
	event_type varchar(20),
	phone varchar(16),
	report_dt date
);

create table dika_meta_update (
    schema_name varchar(30),
    table_name varchar(30),
    max_update_dt timestamp(0)
);

