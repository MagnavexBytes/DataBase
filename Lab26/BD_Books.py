import pprint
import sqlite3
conn = sqlite3.connect('Lab26/BD_Books.sqlite')
c = conn.cursor()
pp = pprint.PrettyPrinter(indent = 1, width = 160, compact = False) 

c.execute('''PRAGMA foreign_keys = 1''')
# c.execute('''PRAGMA foreign_keys = 0''')

c.execute('''drop table if exists editors''')
c.execute('''drop table if exists titles''')
c.execute('''drop table if exists items''')
c.execute('''drop table if exists authors''')
c.execute('''drop table if exists orders''')
c.execute('''drop table if exists customers''')
c.execute('''drop table if exists books''')
c.execute('''drop table if exists employees''')
c.execute('''drop table if exists posts''')
c.execute('''drop table if exists rooms''')

c.execute('''create table if not exists posts (
          p_id  integer,
          p_post  varchar(30) not null,
          p_sal  numeric(8,2)  not null,
            constraint PK_posts_p_id primary key(p_id),
            constraint CK_posts_p_sal check(p_sal > 0))''')

c.execute('''create table if not exists rooms (
          r_no numeric(3) not null,
          r_tel varchar(10),
            constraint UQ_rooms unique(r_no, r_tel))''')

c.execute('''create table if not exists employees (
          e_tab numeric(4),
          e_fname varchar(20) not null,
          e_lname varchar(30) not null,
          e_born date,
          e_gender char(1) not null check(e_gender in ('м','ж')),
          e_post numeric(3) default 5,
          e_room numeric(3),
          e_tel varchar(10),
          e_inn char(12) not null,
          e_passp char(12) not null,
          e_org varchar(30) not null,
          e_pdate date not null,
          e_addr varchar(50),
            constraint PK_employees_e_tab primary key(e_tab),
            constraint FK_employees_e_fname foreign key(e_post) references posts (p_id)
              on delete set default on update set default, 
            constraint FK_employees_room_tel foreign key(e_room,e_tel) references rooms(r_no,r_tel))''')

c.execute('''create table if not exists customers (
          c_id integer,
          c_name varchar(30) not null,
          c_addr varchar(30) not null,
            constraint PK_customers_c_id primary key(c_id))''')

c.execute('''create table if not exists authors (
          a_id integer,
          a_fname varchar(20) not null,
          a_lname varchar(30) not null,
          a_inn char(12),
          a_passp char(12) not null,
          a_org varchar(30) not null,
          a_pdate date not null,
          a_addr varchar(50) not null,
          a_tel varchar(30),
            constraint PK_authors primary key(a_id),
            constraint UQ_authors_a_inn unique(a_inn))''')

c.execute('''create table if not exists books (
          b_contract int(6),
          b_date date not null,
          b_man numeric(4) check (b_man in (1003, 1004)),
          b_title varchar(40) not null,
          b_price numeric(6, 2),
          b_advance numeric(10, 2),
          b_fee numeric(8, 2),
          b_publ date,
          b_circul int(5),
          b_edit numeric(4) check (b_edit in (1006)),
          b_rest int(5), 
            constraint PK_books_contract primary key(b_contract),
            constraint FK_books_man foreign key(b_man) references employees(e_tab) 
              on delete set null on update cascade,
            constraint FK_books_man foreign key(b_edit) references employees(e_tab))''')

c.execute('''create table if not exists orders (
          o_id integer,
          o_company numeric(4) default 5,
          o_date date not null,
          o_ready date,
            constraint PK_orders_id primary key(o_id),
            constraint FK_orders_company foreign key(o_company) references customers(c_id) 
              on delete set default on update set default)''')

c.execute('''create table if not exists titles (
          t_contract int(6),
          t_id int(4),
          t_number int(1) not null,
          t_percent int(3),
            constraint PK_titles primary key(t_contract, t_id),
            constraint CK_titles_percent check(t_percent >= 0 and t_percent <= 100),
            constraint FK_titles_contract foreign key(t_contract) references books(b_contract),
            constraint FK_titles_id foreign key(t_id) references authors(a_id))''')

c.execute('''create table if not exists items (
          i_id int(6),
          i_contract int(6),
          i_count int(4) not null,
            constraint PK_items primary key(i_id, i_contract),
            constraint FK_items_id foreign key(i_id) references orders(o_id),
            constraint FK_items_contract foreign key(i_contract) references books(b_contract))''')

c.execute('''create table if not exists editors (
          e_contract int(6),
          e_id int(4),
            constraint PK_editors primary key(e_contract, e_id),
            constraint FK_editors_contract foreign key(e_contract) references books(b_contract),
            constraint FK_editors_id foreign key(e_id) references employees(e_tab) 
              on delete set null on update cascade)''')

posts = [('editor', 100.2), 
         ('manager', 200.2), 
         ('director', 300.2), 
         ('main editor', 150.2),
         ('test', 350.2)]
c.executemany("INSERT INTO posts(p_post, p_sal) VALUES(?, ?)", posts)
conn.commit()

rooms = [(1, '555-551'), 
         (2, '555-552'), 
         (3, '555-553'), 
         (4, '555-554'), 
         (5, '555-555'), 
         (6, '555-556')]
c.executemany("INSERT INTO rooms VALUES(?, ?)", rooms)
conn.commit()


employees = [(1001, 'Мирон', 'Фролов', '01.01.1980', 'м', 1, 1, '555-551', '1234567890', '7504 12341', 'abracadabra', '01.01.1999', 'Makeeva 34'),
             (1002, 'Игорь', 'Фролов', '01.01.1981', 'м', 1, 2, '555-552', '1234567891', '7504 12342', 'abracadabra', '01.01.1998', 'Makeeva 35'),
             (1003, 'Иван', 'Иванов', '01.01.1982', 'м', 2, 3, '555-553', '1234567892', '7504 12343', 'abracadabra', '01.01.1997', 'Makeeva 36'),
             (1004, 'Мирон', 'Соколов', '01.01.1983', 'м', 2, 4, '555-554', '1234567893', '7504 12344', 'abracadabra', '01.01.1996', 'Makeeva 37'),
             (1005, 'Виктор', 'Дремин', '01.01.1984', 'м', 3, 5, '555-555', '1234567894', '7504 12345', 'abracadabra', '01.01.1995', 'Makeeva 38'),
             (1006, 'Дмитрий', 'Сидоров', '01.01.1985', 'м', 4, 6, '555-556', '1234567895', '7504 12346', 'abracadabra', '01.01.1994', 'Makeeva 39')]
c.executemany("INSERT INTO employees VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", employees)
conn.commit()

books = [(100001,'2021-01-12', 1004, 'Стихи о любви', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100002, '2021-01-12', 1003, 'Собрание сочинений, том 2', 950, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100003, '2021-01-12', 1004, 'Собрание сочинений, том 3', 300, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100004, '2021-01-12', 1004, 'Русская поэзия', 1450, 2000000, 100000, '2021-04-01', 3000, 1006, 3000),
         (100005, '2021-01-12', 1003, 'Машенька', 1350, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100006, '2021-01-12', 1004, 'Доктор Живаго', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100007, '2021-01-12', 1003, 'Наши', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100008, '2021-01-12', 1004, 'Приглашение на казнь', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100009, '2021-01-12', 1004, 'Лолита', 950, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100010, '2021-01-12', 1003, 'Темные аллеи', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100011, '2021-01-12', 1004, 'Дар', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100012, '2021-01-12', 1004, 'Сын вождя', 450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100013, '2021-01-12', 1003, 'Эмигранты', 1450, 2000000, 100000, '2021-04-01', 1000, 1006, 1000),
         (100014, '2021-04-01', 1003, 'Горе от ума', 1450, 2000000, 100000, '2021-01-12', 1000, 1006, 1000)]
c.executemany("INSERT INTO books VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", books)
conn.commit()

c.execute('''insert into customers(c_name, c_addr) values 
          ('Заказчик1', 'Адрес1'),
          ('Заказчик2', 'Адрес2'),
          ('Заказчик3', 'Адрес3'),
          ('Заказчик4', 'Адрес4'),
          ('ЗаказчикТест', 'АдресТест')''')

c.execute('''insert into authors(a_fname, a_lname, a_inn, a_passp, a_org, a_pdate, a_addr, a_tel) values 
          ('Фамилия1', 'Имя1', '741234123411', '1234 N123456', 'Организация1', '2000-01-01', 'адрес1', '+798111111'),
          ('Фамилия2', 'Имя2', '741234123412', '1234 N123456', 'Организация2', '2000-01-01', 'адрес1', '+798111111'),
          ('Фамилия3', 'Имя3', '741234123413', '1234 N123456', 'Организация3', '2000-01-01', 'адрес1', '+798111111'),
          ('Набоков', 'Владимир', '741234123414', '1234 N123456', 'Организация4', '2000-01-01', 'адрес1', '+798111111'),
          ('Грибоедов', 'Александр', '741234123415', '1234 N123456', 'Организация5', '2000-01-01', 'адрес1', '+798111111'),
          ('Пастернак', 'Борис', '741234123416', '1234 N123456', 'Организация6', '2000-01-01', 'адрес1', '+798111111'),
          ('Цветаева', 'Марина', '741234123417', '1234 N123456', 'Организация7', '2000-01-01', 'адрес1', '+798111111')''')

c.execute('''insert into orders(o_company, o_date, o_ready) values 
          (4, '2001-02-03', '2001-05-03'),
          (2, '2001-01-03', '2001-04-03'),
          (1, '2001-05-03', '2001-06-03'),
          (2, '2001-08-03', '2001-09-03')''')

c.execute('''insert into items values 
          (1, 100005, 50),
          (1, 100009, 60),
          (1, 100014, 60),
          (2, 100005, 40),
          (2, 100001, 100),
          (2, 100002, 10),
          (3, 100002, 10),
          (3, 100006, 10),
          (4, 100011, 80)''')
conn.commit()

editors = [(100001, 1001),
           (100002, 1001),
           (100003, 1001),
           (100004, 1001),
           (100005, 1001),
           (100006, 1001),
           (100007, 1001),
           (100008, 1001),
           (100009, 1001),
           (100010, 1001),
           (100011, 1001),
           (100012, 1001),
           (100013, 1001),
           (100014, 1001),
           (100001, 1002),
           (100002, 1002),
           (100003, 1002),
           (100004, 1002),
           (100005, 1002),
           (100006, 1002),
           (100007, 1002),
           (100008, 1002),
           (100009, 1002),
           (100010, 1002)]

c.executemany("INSERT INTO editors VALUES(?, ?)", editors)
conn.commit()

c.execute('''insert into titles values
          (100005, 2, 1, 100),
          (100009, 2, 1, 100),
          (100011, 3, 1, 100),
          (100014, 2, 1, 100),
          (100006, 3, 1, 100),
          (100001, 1, 1, 100),
          (100002, 1, 1, 100)''')
conn.commit()

# print("______________________________________")
# print("Таблица системная (sqlite_master)")
# c.execute('''select name, sql from sqlite_master''')
# pp.pprint(c.fetchall())

# c.execute('''atler table posts rename to new_posts''')

# print("______________________________________")
# print("Таблица системная (sqlite_master)")
# c.execute('''select name, sql from sqlite_master''')
# pp.pprint(c.fetchall())

# c.execute('''insert into employees values (1007,'Иван','Иванов','01.11.1985','м',5,6,'555-556','1234567895','7504 12346','abracadabra','01.01.1994','Makeeva 39')''')
# conn.commit()

# c.execute('''delete from posts where p_id = 1''')
# pp.pprint(c.fetchall())
# c.execute('''delete from posts where p_id = 2''')
# pp.pprint(c.fetchall())

# c.execute('''update posts set p_id = 10 where p_id = 1''')
# pp.pprint(c.fetchall())

# c.execute('''update posts set p_id = p_id * 10''')
# pp.pprint(c.fetchall())
# c.execute('''update posts set p_id = p_id * 10 where p_id != 5''')
# pp.pprint(c.fetchall())

# c.execute('''update customers set c_id = c_id * 100''')
# pp.pprint(c.fetchall())
# c.execute('''delete from customers where c_id = 1''')
c.execute('''select * from customers''')
pp.pprint(c.fetchall())
c.execute('''select * from orders''')
pp.pprint(c.fetchall())
c.execute('''select * from items''')
pp.pprint(c.fetchall())

# c.execute('''select * from posts''')
# pp.pprint(c.fetchall())
# c.execute('''select * from employees''')
# pp.pprint(c.fetchall())
# c.execute('''select * from books''')
# pp.pprint(c.fetchall())
# c.execute('''select * from editors''')
# pp.pprint(c.fetchall())

conn.close()
