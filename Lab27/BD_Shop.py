import pprint
import sqlite3
conn = sqlite3.connect('Lab27/BD_Shop.sqlite')
c = conn.cursor()
pp = pprint.PrettyPrinter(indent = 1, width = 160, compact = False) 

c.execute('''PRAGMA foreign_keys = 1''')

c.execute('''drop table if exists magazine_sales''')
c.execute('''drop table if exists magazine_incoming''')
c.execute('''drop table if exists incoming''')
c.execute('''drop table if exists sale''')
c.execute('''drop table if exists prices''')
c.execute('''drop table if exists products''')
c.execute('''drop table if exists vendors''')
c.execute('''drop table if exists customers''')

c.execute('''drop table if exists new_prices''')

# Таблицы
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
            constraint FK_magazine_incoming_id_product FOREIGN KEY (id_product) REFERENCES Products(id_product))
''')


# Данные
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
c.executemany('''INSERT INTO prices (id_product, date_price_changes, price) VALUES (?,?,?)''', prices_m)

incoming_m = [('3'), ('1'), ('2')]
c.executemany('''INSERT INTO incoming (id_vendor) VALUES (?)''', incoming_m)

# Задания 
pp.pprint("")
pp.pprint("____________________________________[Задание 1]____________________________________")

pp.pprint("")
pp.pprint("------------prices------------")
c.execute('''Select * from prices''')
pp.pprint(c.fetchall())

c.execute('''ALTER TABLE prices RENAME TO new_prices''')

pp.pprint("")
pp.pprint("------------new_prices------------")
c.execute('''Select * from new_prices''')
pp.pprint(c.fetchall())

# c.execute('''select name, sql from sqlite_master''')
# pp.pprint(c.fetchall())

pp.pprint("")
pp.pprint("____________________________________[Задание 2]____________________________________")

pp.pprint("")
pp.pprint("------------customers------------")
c.execute('''Select * from customers''')
pp.pprint(c.fetchall())

c.execute('''ALTER TABLE customers ADD age INT 
          DEFAULT 18 
          constraint CK_customers_age CHECK (age > 0 and age < 100)
''')

c.execute('''ALTER TABLE customers ADD Phone VARCHAR(20)
          DEFAULT "no"
''')

pp.pprint("")
pp.pprint("------------customers------------")
c.execute('''Select * from customers''')
pp.pprint(c.fetchall())

pp.pprint("")
pp.pprint("____________________________________[Задание 3]____________________________________")

pp.pprint("")
pp.pprint("------------customers------------")
c.execute('''Select * from customers''')
pp.pprint(c.fetchall())

c.execute('''ALTER TABLE customers DROP age''')
c.execute('''ALTER TABLE customers DROP Phone''')

pp.pprint("")
pp.pprint("------------customers------------")
c.execute('''Select * from customers''')
pp.pprint(c.fetchall())

pp.pprint("")
pp.pprint("____________________________________[Задание 4]____________________________________")

pp.pprint("")
pp.pprint("------------magazine_sales------------")
c.execute('''Select * from magazine_sales''')
pp.pprint(c.fetchall())

c.execute('''ALTER TABLE magazine_sales RENAME COLUMN quantity TO N''')

pp.pprint("")
pp.pprint("------------magazine_sales------------")
c.execute('''Select * from magazine_sales''')
pp.pprint(c.fetchall())

pp.pprint("")
pp.pprint("____________________________________[Задание 5]____________________________________")

pp.pprint("")
pp.pprint("------------vendors------------")
c.execute('''Select * from vendors''')
pp.pprint(c.fetchall())

# c.execute('''CREATE UNIQUE INDEX unique_index on vendors (name)''')
# c.execute('''ALTER TABLE vendors ADD CONSTRAINT unique_name UNIQUE (name)''')
# Добавьте ограничение уникальности на пару столбцов name и city таблицы vendors.
# Добавьте ограничение на значение столбца quantity таблицы magazine_sales (от 0 до 10), по умолчанию 1.

# c.execute('''ALTER TABLE vendors ADD Phone''')

pp.pprint("")
pp.pprint("------------vendors------------")
c.execute('''Select * from vendors''')
pp.pprint(c.fetchall())

conn.close()