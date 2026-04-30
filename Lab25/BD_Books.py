import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent = 2, width = 60, compact = False)
pp_wide = pprint.PrettyPrinter(indent = 2, width = 180, compact = False)
conn = sqlite3.connect('Lab25/BD_Books.sqlite')
c = conn.cursor()
c.execute('''PRAGMA foreign_keys = 1''')


c.execute('''drop table if exists titles''')
c.execute('''drop table if exists editors''')
c.execute('''drop table if exists items''')
c.execute('''drop table if exists orders''')
c.execute('''drop table if exists books''')
c.execute('''drop table if exists authors''')
c.execute('''drop table if exists employees''')
c.execute('''drop table if exists authors''')
c.execute('''drop table if exists posts''')
c.execute('''drop table if exists rooms''')
c.execute('''drop table if exists customers''')

c.execute('''
create table if not exists posts (
          p_id  integer, 
          p_post  varchar(30) not null,
          p_sal  numeric(8,2)  not null,
            Constraint CK_Posts_p_sal check(p_sal > 0),
            Constraint PK_Posts_p_id  primary key (p_id)
)''')

c.execute('''
create table if not exists rooms (
          r_no numeric(3) not null,
          r_tel varchar(10),
            Constraint UQ_Rooms_R_no_r_tel unique ( r_no, r_tel)
)''')

c.execute('''
create table if not exists employees (
          e_tab numeric(4),
          e_fname varchar(20) not null,
          e_lname varchar(30) not null,
          e_born date,
          e_gender char(1) not null,
          e_post numeric(3),
          e_room numeric(3),
          e_tel varchar(10),
          e_inn char(12) not null,
          e_passp char(12) not null,
          e_org varchar(30) not null,
          e_pdate date not null,
          e_addr varchar(50),
            Constraint CK_Employees_e_gender check(e_gender in ('ж','м','Ж','М','f','m','F','M')),
            Constraint PK_Employees_E_tab primary key(e_tab),
            Constraint FK_Employees_e_post foreign key(e_post) references posts (p_id), 
            Constraint FK_Employees_e_room_e_tel foreign key(e_room,e_tel) references rooms(r_no,r_tel)
)''')

c.execute('''
create table if not exists customers (
          c_id integer not null,
          c_name char(30) not null,
          c_addr char(30) not null,
          Constraint PK_Customers_c_id primary key (c_id)
)''')

c.execute('''
create table if not exists authors (
          a_id integer not null,
          a_fname char(20) not null,
          a_lname char(30) not null,
          a_inn char(12),
          a_passp char(12) not null,
          a_org char(30) not null,
          a_pdate date not null,
          a_addr char(50) not null,
          a_tel char(30),
            Constraint PK_Authors_a_id primary key (a_id)
)''')

c.execute('''
create table if not exists books (
          b_contract numeric(6) not null,
          b_date date not null,
          b_man numeric(4),
          b_title char(40) not null,
          b_price numeric(6, 2),
          b_advance numeric(10, 2),
          b_fee numeric(8, 2),
          b_publ date,
          b_circul numeric(5),
          b_edit numeric(4),
          b_rest numeric(5),
            Constraint CK_Books_b_rest check (b_rest >= 0),
            Constraint CK_Books_b_fee check (b_fee >= 0),
            Constraint PK_Books_b_contract primary key (b_contract),
            Constraint FK_Books_b_man foreign key (b_man) references employees (e_tab),
            Constraint FK_Books_b_edit foreign key (b_edit) references employees (e_tab)
)''')

c.execute('''
create table if not exists orders (
          o_id integer not null,
          o_company numeric(4),
          o_date date not null,
          o_ready date,
            Constraint PK_Orders_o_id primary key (o_id),
            Constraint FK_Orders_o_company foreign key (o_company) references cutomers (c_id)
)''')

c.execute('''
create table if not exists titles (
          t_contract numeric(6),
          t_id numeric(4),
          t_number numeric(4),
          t_percent numeric(3),
            Constraint CK_Titles_t_percent check (t_percent > 0),
            Constraint PK_Titles_t_id_t_contract primary key (t_id, t_contract),
            Constraint FK_Titles_t_contract foreign key (t_contract) references books (b_contract),
            Constraint FK_Titles_t_id foreign key (t_id) references authors (a_id)
)''')

c.execute('''
create table if not exists items (
          i_id numeric(6),
          i_contract numeric(6),
          i_count numeric(4) not null,
            Constraint CK_Items_i_count check (i_count > 0),
            Constraint PK_Items_i_id_i_contract primary key (i_id, i_contract),
            Constraint FK_Items_i_id foreign key (i_id) references orders (o_id),
            Constraint FK_Items_i_contract foreign key (i_contract) references books (b_contract)
)''')

c.execute('''
create table if not exists editors (
          e_id numeric(4),
          e_contract numeric(6),
            Constraint PK_Editors_e_id_e_contract primary key (e_id, e_contract),
            Constraint FK_Editors_e_id foreign key (e_id) references employees (e_tab),
            Constraint FK_Editors_e_contract foreign key (e_contract) references books (b_contract)
)''')

c.execute('''Insert into posts (p_post, p_sal) values
          ('editor',100.2),
          ('manager',200.2),
          ('director',300.2),
          ('main editor',150.2)
''')

c.execute('''Insert into rooms values
          (1,'555-551'),
          (2,'555-552'),
          (3,'555-553'),
          (4,'555-554'),
          (5,'555-555'),
          (6,'555-556')
''')

c.execute('''Insert into employees values
          (1001, 'Мирон', 'Фролов', '01.01.1980', 'м', 1, 1, '555-551', '1234567890', '7504 12341', 'abracadabra', '01.01.1999', 'Makeeva 34'),
          (1002, 'Игорь', 'Фролов', '01.01.1981', 'м', 1, 2, '555-552', '1234567891', '7504 12342', 'abracadabra', '01.01.1998', 'Makeeva 35'),
          (1003, 'Иван', 'Иванов', '01.01.1982', 'м', 2, 3, '555-553', '1234567892', '7504 12343', 'abracadabra', '01.01.1997', 'Makeeva 36'),
          (1004, 'Мирон', 'Соколов', '01.01.1983', 'м', 2, 4, '555-554', '1234567893', '7504 12344', 'abracadabra', '01.01.1996', 'Makeeva 37'),
          (1005, 'Виктор', 'Дремин', '01.01.1984', 'м', 3, 5, '555-555', '1234567894', '7504 12345', 'abracadabra', '01.01.1995', 'Makeeva 38'),
          (1006, 'Дмитрий', 'Сидоров', '01.01.1985', 'м', 4, 6, '555-556', '1234567895', '7504 12346', 'abracadabra', '01.01.1994', 'Makeeva 39')
''')

c.execute('''Insert into books values
          (100001, '2021-01-12', 1004, 'Стихи о любви', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100002, '2021-01-12', 1003, 'Собрание сочинений, том 2', 950, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100003, '2021-01-12', 1004, 'Собрание сочинений, том 3', 300, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100004, '2021-01-12', 1003, 'Русская поэзия', 1450, 2000000, 100000, '2021-04-01', 3000, 1006, 3000),
          (100005, '2021-01-12', 1004, 'Машенька',1350, 2000000,100000, '2021-04-01', 1000, 1006, 1000),
          (100006, '2021-01-12', 1004, 'Доктор Живаго', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100007, '2021-01-12', 1003, 'Наши', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100008, '2021-01-12', 1004, 'Приглашение на казнь', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100009, '2021-01-12', 1004, 'Лолита', 950, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100010, '2021-01-12', 1003, 'Темные аллеи', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100011, '2021-01-12', 1004, 'Дар', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100012, '2021-01-12', 1004, 'Сын вождя', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100013, '2021-01-12', 1003, 'Эмигранты', 1450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
          (100014, '2021-04-01', 1004, 'Горе от ума', 1450, 2000000, 100000, '2021-01-12', 1000, 1006, 1000)
''')

conn.commit()
print("______________________________________")
print("Table posts")
c.execute('''Select * from posts''')
pp.pprint(c.fetchall())
print("______________________________________")
print("Table rooms")
c.execute('''Select * from rooms''')
pp.pprint(c.fetchall())
print("______________________________________")
print("Table employees")
c.execute('''Select * from employees''')
pp_wide.pprint(c.fetchall())
print("______________________________________")
print("Table books")
c.execute('''Select * from books''')
pp_wide.pprint(c.fetchall())
conn.close() 
