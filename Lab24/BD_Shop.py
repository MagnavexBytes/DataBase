import sqlite3 
import pprint
pp = pprint.PrettyPrinter(indent = 1, width = 100, compact = False)
conn = sqlite3.connect('Lab24/BD_SHOP.sqlite') 
c = conn.cursor()
c.execute('''PRAGMA foreign_keys = 1''')

# c.execute('''drop table if exists magazine_sales''')
# c.execute('''drop table if exists magazine_incoming''')
# c.execute('''drop table if exists incoming''')
# c.execute('''drop table if exists sale''')
# c.execute('''drop table if exists prices''')
# c.execute('''drop table if exists products''')
# c.execute('''drop table if exists vendors''')
# c.execute('''drop table if exists customers''')

c.execute('''create table if not exists customers (
          id_customer integer NOT NULL,
          name char(50) NOT NULL,
           email char(50) NOT NULL,
          constraint UQ_Customers_email unique(email),
          constraint PK_customers_id_customer PRIMARY KEY (id_customer))''')

c.execute('''create table if not exists vendors (
          id_vendor integer NOT NULL,
          name char(50) NOT NULL,
          city char(30) NOT NULL,
          address char(100) NOT NULL,
          constraint PK_Vendors_id_vendor PRIMARY KEY (id_vendor))''')

c.execute('''create table if not exists products (
          id_product integer NOT NULL,
          name char(100) NOT NULL,
          author char(50) NOT NULL,
          constraint PK_Products_id_product PRIMARY KEY (id_product))''')

c.execute('''create table if not exists prices (
          id_product int NOT NULL,
          date_price_changes date NOT NULL,
          price double NOT NULL,
          constraint CK_Prices_price CHECK(price > 0),
          constraint PK_Prices_id_product_date_price_changes PRIMARY KEY (id_product, date_price_changes),
          constraint FK_Prices_id_product FOREIGN KEY (id_product) REFERENCES Products (id_product))''')

c.execute('''create table if not exists sale (
          id_sale integer NOT NULL,
          id_customer int NOT NULL,
          date_sale text NOT NULL DEFAULT current_date,
          constraint PK_Sale_id_sale PRIMARY KEY (id_sale),
          constraint FK_Sale_id_customer FOREIGN KEY (id_customer) REFERENCES Customers (id_customer))''')

c.execute('''create table if not exists incoming (
          id_incoming integer NOT NULL,
          id_vendor int NOT NULL,
          date_incoming text NOT NULL default current_date,
          constraint PK_Incoming_id_incoming PRIMARY KEY (id_incoming),
          constraint FK_Incoming_id_vendor FOREIGN KEY (id_vendor) REFERENCES Vendors(id_vendor))''')

c.execute('''create table if not exists magazine_sales (
          id_sale int NOT NULL,
          id_product int NOT NULL,
          quantity int NOT NULL,
          constraint CK_magazine_sales CHECK(quantity > 0)
          constraint PK_magazine_sales_id_sale_id_product PRIMARY KEY (id_sale, id_product),
          constraint FK_magazine_sales_id_sale FOREIGN KEY (id_sale) REFERENCES Sale(id_sale),
          constraint FK_magazine_sales_id_product FOREIGN KEY (id_product) REFERENCES products(id_product))''')
  
c.execute('''create table if not exists magazine_incoming (
          id_incoming int NOT NULL,
          id_product int NOT NULL,
          quantity int NOT NULL,
          constraint CK_magazine_incoming CHECK(quantity > 0)
          constraint PK_magazine_incoming_id_incoming_id_product PRIMARY KEY (id_incoming, id_product),
          constraint FK_magazine_incoming_id_incoming FOREIGN KEY (id_incoming) REFERENCES Incoming(id_incoming),
          constraint FK_magazine_incoming_id_product FOREIGN KEY (id_product) REFERENCES Products(id_product))''')

c.execute('''delete from magazine_sales''')
c.execute('''delete from magazine_incoming''')
c.execute('''delete from incoming''')
c.execute('''delete from sale''')
c.execute('''delete from prices''')
c.execute('''delete from products''')
c.execute('''delete from vendors''')
c.execute('''delete from customers''')

vendors_m = [('Вильямс', 'Москва', 'ул.Лесная, д.43'),
             ('Дом печати', 'Минск', 'пр.Ф.Скорины, д.18'),
             ('БХВ-Петербург', 'Санкт-Петербург', 'ул.Есенина, д.5')]
c.executemany('''INSERT INTO vendors (name, city, address) VALUES (?,?,?)''' , vendors_m)

customers_m = [('Иванов Сергей', 'sergo@mail.ru'),
               ('Ленская Катя', 'lenskay@yandex.ru'),
               ('Демидов Олег', 'demidov@gmail.ru'),
               ('Афанасьев Виктор', 'victor@mail.ru'),
               ('Пажская Вера', 'verap@rambler.ru')]
c.executemany('''INSERT INTO customers (name, email) VALUES (?,?)''' , customers_m)
  
products_m = [('Стихи о любви', 'Андрей Вознесенский'),
              ('Собрание сочинений, том 2', 'Андрей Вознесенский'),
              ('Собрание сочинений, том 3', 'Андрей Вознесенский'),
              ('Русская поэзия', 'Николай Заболоцкий'),
              ('Машенька', 'Владимир Набоков'),
              ('Доктор Живаго', 'Борис Пастернак'),
              ('Наши', 'Сергей Довлатов'),
              ('Приглашение на казнь', 'Владимир Набоков'),
              ('Лолита', 'Владимир Набоков'),
              ('Темные аллеи', 'Иван Бунин'),
              ('Дар', 'Владимир Набоков'),
              ('Сын вождя', 'Юлия Вознесенская'),
              ('Эмигранты', 'Алексей Толстой'),
              ('Горе от ума', 'Александр Грибоедов'),
              ('Анна Каренина', 'Лев Толстой'),
              ('Повести и рассказы', 'Николай Лесков'),
              ('Антоновские яблоки', 'Иван Бунин'),
              ('Мертвые души', 'Николай Гоголь'),
              ('Три сестры', 'Антон Чехов'),
              ('Беглянка', 'Владимир Даль'),
              ('Идиот', 'Федор Достоевский'),
              ('Братья Карамазовы', 'Федор Достоевский'),
              ('Ревизор', 'Николай Гоголь'),
              ('Гранатовый браслет', 'Александр Куприн')]
c.executemany('''INSERT INTO products (name, author) VALUES (?,?)''' , products_m)

prices_m = [(12, '2024-04-12', 85),
            (13, '2024-04-12', 135),
            (14, '2024-04-12', 100),
            (15, '2024-04-12', 90),
            (16, '2024-04-12', 75),
            (17, '2024-04-12', 90),
            (7, '2024-04-11', 95),
            (8, '2024-04-11', 100),
            (9, '2024-04-11', 79),
            (10, '2024-04-11', 49),
            (11, '2024-04-11', 105),
            (21, '2024-04-11', 105),
            (22, '2024-04-11', 70),
            (23, '2024-04-11', 65),
            (24, '2024-04-11', 130),
            (1, '2024-04-10', 100),
            (2, '2024-04-10', 130),
            (3, '2024-04-10', 90),
            (4, '2024-04-10', 100),
            (5, '2024-04-10', 110),
            (6, '2024-04-10', 85),
            (18, '2024-04-10', 150),
            (19, '2024-04-10', 140),
            (20, '2024-04-10', 85)]
c.executemany('''INSERT INTO prices (id_product, date_price_changes, price) VALUES (?,?,?)''' , prices_m)

c.execute('''INSERT INTO prices (id_product, date_price_changes, price)
          select id_product, date('2025-01-01'), price*1.2 
          from prices''')

c.execute('''INSERT INTO prices (id_product, date_price_changes, price)
          select id_product, date('now'), price * 2 
          from prices as p 
          where date_price_changes = (select max(date_price_changes) 
              from prices 
              where id_product = p.id_product) ''')

c.execute('''INSERT INTO incoming (id_vendor) VALUES (3),(1),(2)''')

magazine_incoming=[(1, 1, 10),
                   (1, 2, 5),
                   (1, 3, 7),
                   (1, 4, 10),
                   (1, 5, 10),
                   (1, 6, 8),
                   (1, 18, 8),
                   (1, 19, 8),
                   (1, 20, 8),
                   (2, 7, 10),
                   (2, 8, 10),
                   (2, 9, 6),
                   (2, 10, 10),
                   (2, 11, 10),
                   (2, 21, 10),
                   (2, 22, 10),
                   (2, 23, 10),
                   (2, 24, 10),
                   (3, 12, 10),
                   (3, 13, 10),
                   (3, 14, 10),
                   (3, 15, 10),
                   (3, 16, 10),
                   (3, 17, 10)]
c.executemany('''INSERT INTO magazine_incoming (id_incoming, id_product, quantity) VALUES (?,?,?)''' , magazine_incoming)

c.execute('''INSERT INTO magazine_incoming (id_incoming, id_product, quantity)
select 2, id_product, quantity from magazine_incoming where id_incoming=3''')

c.execute('''INSERT INTO sale (id_customer) VALUES (2), (3), (5), (3), (2), (1)''')

magazine_sales = [(1, 1, 1),
                  (1, 5, 1),
                  (1, 7, 1),
                  (2, 2, 1),
                  (3, 1, 1),
                  (3, 7, 1),
                  (4, 17, 1),
                  (4, 10, 1),
                  (5, 12, 1),
                  (6, 10, 1)]
c.executemany('''INSERT INTO magazine_sales (id_sale, id_product, quantity) VALUES (?,?,?)''' , magazine_sales)

print("______________________________________")
print("Таблица Покупатели (Customers)")
c.execute('''select * from customers''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Поставщики (Vendors)")
c.execute('''select * from vendors''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Товары (Products)")
c.execute('''select * from products''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Цены (Prices)")
c.execute('''select * from prices order by 1''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Покупки (Sale)")
c.execute('''select * from sale''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Поставки (Incoming)")
c.execute('''select * from incoming ''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Журнал покупок (Magazine_sales)")
c.execute('''select * from magazine_sales''')
pp.pprint(c.fetchall())

print("______________________________________")
print("Таблица Журнал поставок (Magazine_incoming)")
c.execute('''select * from magazine_incoming order by 1 ''')
pp.pprint(c.fetchall())

# print("______________________________________")
# print("Таблица системная (sqlite_master)")
# c.execute('''select name, sql from sqlite_master''')
# pp.pprint(c.fetchall())

conn.commit()
conn.close() 