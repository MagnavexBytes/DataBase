# Стандартный шаблон
import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent = 1, width = 80, compact = False) 
# Открытие передачи
conn = sqlite3.connect('Lab23/BD_Shop.sqlite') 
c = conn.cursor() 

# Используем команду проверки внешних ключей
c.execute('''PRAGMA foreign_keys = 1''')

# Удаляем таблицы целиком, начиная с самых зависимых
# c.execute('''drop table if exists vendors''')
# c.execute('''drop table if exists customers''')
# c.execute('''drop table if exists incoming''')
# c.execute('''drop table if exists sales''')
# c.execute('''drop table if exists products''')
# c.execute('''drop table if exists magazine_sales''')
# c.execute('''drop table if exists magazine_incoming''')
# c.execute('''drop table if exists prices''')
# conn.commit()

# Создаём таблицу customers
c.execute('''CREATE TABLE IF NOT EXISTS customers (
  id_customer integer NOT NULL, 
  name char(50) NOT NULL,
  email char(50) NOT NULL 
          CONSTRAINT UQ_email UNIQUE,
          CONSTRAINT PK_id_customer PRIMARY KEY (id_customer))''')

# Создаём таблицу vendors
c.execute('''CREATE TABLE IF NOT EXISTS vendors (
  id_vendor integer NOT NULL,
  name char(50) NOT NULL,
  city char(30) NOT NULL,
  address char(100) NOT NULL,
          CONSTRAINT PK_id_vendor PRIMARY KEY (id_vendor))''')

# Создаём таблицу products
c.execute('''CREATE TABLE IF NOT EXISTS products (
  id_product integer NOT NULL,
  name char(100) NOT NULL,
  author char(50) NOT NULL,
          CONSTRAINT PK_id_product PRIMARY KEY (id_product))''')

# Создаём таблицу prices
c.execute('''create table if not exists prices (
  id_product int NOT NULL,
  date_price_changes date NOT NULL,
  price double NOT NULL,
  constraint CK_Prices_price CHECK(price>0),
  constraint PK_Prices_id_product_date_price_changes PRIMARY KEY (id_product, date_price_changes),
  constraint FK_Prices_id_product FOREIGN KEY (id_product) REFERENCES Products (id_product))''')

# Создаём таблицу sale
c.execute('''CREATE TABLE IF NOT EXISTS sale (
  id_sale integer NOT NULL,
  id_customer int NOT NULL,
  date_sale text NOT NULL
          DEFAULT (current_date),
          CONSTRAINT PK_id_sale PRIMARY KEY (id_sale),
          CONSTRAINT FK_id_customer FOREIGN KEY (id_customer) REFERENCES customers (id_customer))''')

# Создаём таблицу incoming
c.execute('''CREATE TABLE IF NOT EXISTS incoming (
  id_incoming integer NOT NULL,
  id_vendor int NOT NULL,
  date_incoming text NOT NULL
          DEFAULT (current_date),
          CONSTRAINT PK_id_incoming PRIMARY KEY (id_incoming),
          CONSTRAINT FK_id_vendor FOREIGN KEY (id_vendor) REFERENCES vendors (id_vendor))''')
  
# Создаём таблицу magazine_sales
c.execute('''CREATE TABLE IF NOT EXISTS magazine_sales (
  id_sale int NOT NULL,
  id_product int NOT NULL,
  quantity int NOT NULL
          CONSTRAINT CK_quantity CHECK (quantity > 0),
          CONSTRAINT PK_magazine_sales PRIMARY KEY (id_sale, id_product),
          CONSTRAINT FK_id_sale FOREIGN KEY (id_sale) REFERENCES sale (id_sale),
          CONSTRAINT FK_id_product FOREIGN KEY (id_product) REFERENCES products (id_product))''')

# Создаём таблицу magazine_incoming
c.execute('''CREATE TABLE IF NOT EXISTS magazine_incoming (
  id_incoming int NOT NULL,
  id_product int NOT NULL,
  quantity int NOT NULL
          CONSTRAINT CK_quantity CHECK (quantity > 0),
          CONSTRAINT PK_magazine_incoming PRIMARY KEY (id_incoming, id_product),
          CONSTRAINT FK_id_incoming FOREIGN KEY (id_incoming) REFERENCES incoming (id_incoming),
          CONSTRAINT FK_id_product FOREIGN KEY (id_product) REFERENCES products (id_product))''')

# Удаляем строки таблиц
c.execute('''delete from magazine_incoming''')
c.execute('''delete from magazine_sales''')
c.execute('''delete from incoming''')
c.execute('''delete from sale''')
c.execute('''delete from prices''')
c.execute('''delete from products''')
c.execute('''delete from vendors''')
c.execute('''delete from customers''')
conn.commit()

# Вносим значения в vendors
c.execute('''INSERT INTO vendors (name, city, address) VALUES 
          ('Вильямс', 'Москва', 'ул.Лесная, д.43'),
          ('Дом печати', 'Минск', 'пр.Ф.Скорины, д.18'),
          ('БХВ-Петербург', 'Санкт-Петербург', 'ул.Есенина, д.5')''')
conn.commit()

# Вносим значения в customers
c.execute('''INSERT INTO customers (name, email) VALUES 
          ('Иванов Сергей', 'sergo@mail.ru'),
          ('Ленская Катя', 'lenskay@yandex.ru'),
          ('Демидов Олег', 'demidov@gmail.ru'),
          ('Афанасьев Виктор', 'victor@mail.ru'),
          ('Пажская Вера', 'verap@rambler.ru')''')
conn.commit()

# Вносим значения в products
c.execute('''INSERT INTO products (name, author) VALUES
          ('Стихи о любви', 'Андрей Вознесенский'),
          ('Собрание сочинений, том 2', 'Андрей Вознесенский'),
          ('Собрание сочинений, том 3', 'Андрей Вознесенский'),
          ('Русская поэзия', 'Николай Заболоцкий'),
          ('Машенька', 'Владимир Набоков'),
          ('Доктор Живаго', 'Борис Пастернак'),
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
          ('Гранатовый браслет', 'Александр Куприн')''')
conn.commit()

# Вносим значения в prices
prices_BD_prices = [(12, '2024-04-12', 85),
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
c.executemany('''INSERT INTO prices (id_product, date_price_changes, price) VALUES (?,?,?)''', prices_BD_prices)

products_BD_prices = [('Стихи о любви', 'Андрей Вознесенский'),
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
c.executemany('''INSERT INTO products (name, author) VALUES (?,?)''', products_BD_prices)

prices_BD_prices = [(12, '2024-04-12', 85),
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
c.executemany('''INSERT INTO prices (id_product, date_price_changes, price) VALUES (?,?,?)''', prices_BD_prices)

c.execute('''INSERT INTO prices (id_product, date_price_changes, price)
select id_product, date('2025-01-01'), price*1.2 from prices''')
c.execute('''INSERT INTO prices (id_product, date_price_changes, price)
select id_product, date('now'), price*2 from prices as p where date_price_changes = (select max(date_price_changes) from prices where id_product=p.id_product) ''')

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
select 2, id_product, quantity from magazine_incoming where id_incoming = 3''')

c.execute('''INSERT INTO sale (id_customer) VALUES (2), (3), (5), (3), (2), (1)''')

# 5.1
pp.pprint(5.1)
c.execute('''insert into prices (id_product, date_price_changes, price)
          select id_product, "2025-01-01" as date_price_changes, price * 1,2
          from prices as p
          where date_price_changes = (
          select max(date_price_changes) from prices 
          where id_product = p.id_product)
          ''')
c.execute('''select * from prices order by 1, 2''')
pp.pprint(c.fetchall())

# 5.2
pp.pprint(5.2)
c.execute('''insert into prices (id_product, date_price_changes, price)
          select id_product, current_date as date_price_changes, price * 2
          from prices as p
          where date_price_changes = (
          select max(date_price_changes) from prices 
          where id_product = p.id_product)
          ''')
c.execute('''select * from prices order by 1, 2''')
pp.pprint(c.fetchall())

# Вывод содержимого таблиц
# c.execute('''Select * from customers''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from vendors''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from products''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from prices''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from sale''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from incoming''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from magazine_sales''')
# pp.pprint(c.fetchall())
# c.execute('''Select * from magazine_incoming''')
# pp.pprint(c.fetchall())

# Закрытие передачи
conn.close() 