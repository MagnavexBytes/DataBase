# Стандартный шаблон
import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent = 1, width = 80, compact = False) 
# Открытие передачи
conn = sqlite3.connect('Lab22/BD_test.sqlite') 
c = conn.cursor() 

# Используем команду проверки внешних ключей
c.execute('''PRAGMA foreign_keys = 1''')

# Удаляем таблицы целиком, начиная с самых зависимых
c.execute('''drop table if exists t''')
c.execute('''drop table if exists Customers''')
c.execute('''drop table if exists teachers_class''')
c.execute('''drop table if exists teachers''')
c.execute('''drop table if exists job_titles''')
c.execute('''drop table if exists experience''')
conn.commit()


# Задание 1
c.execute('''CREATE TABLE IF NOT EXISTS t (
name CHAR UNIQUE,
num REAL CHECK (num < 100),
i INTEGER DEFAULT 100000,
r REAL NOT NULL CHECK (r >= 200),
no CHAR NOT NULL,
CHECK (r + i >= 400))''')

# Набор значений 1
# t_1 = [('abc', 50, 500000, 210, 'первая строка'),
#         ('abc', '90', 400000, 2210, 'вторая строка')]
# c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_1)
# conn.commit()
# Нарушено ограничение UNIQUE name

# Набор значений 2
t_2 = [(None, 50, 500000, 210, 'первая строка'),
        (None, 90, 400000, 2210, 'вторая строка')]
c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_2)
conn.commit()
# Нарушений нет. В Питоне в массивах используем none вместо null

# Набор значений 3
# t_3 = [('abc', 150, 500000, 210, 'первая строка')]
# c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_3)
# conn.commit()
# Нарушено ограничение CHECK num < 100

# Набор значений 4
# t_4 = [('abd', 50, 500000, None, 'первая строка')]
# c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_4)
# conn.commit()
# Нарушено ограничение NOT NULL r

# Набор значений 5
# t_5 = [('abe', 50, 500000, 10, 'первая строка')]
# c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_5)
# conn.commit()
# Нарушено ограничение CHECK r >= 200

# Набор значений 6
t_6 = [('abf', 50, 500000, 210, 'первая строка')]
c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_6)
conn.commit()
# Нарушений нет

# Набор значений 7
# t_7 = [('abff', 50, 50, 210, 'первая строка')]
# c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_7)
# conn.commit()
# Нарушено ограничение CHECK r + i >= 400

# Набор значений 8
t_8 = [('abfff', 50, 500, 210, 'первая строка')]
c.executemany("INSERT INTO t (name, num, i, r, no) VALUES (?,?,?,?,?)", t_8)
conn.commit()
# Нарушений нет

# Набор значений 9
t_9 = [('abbff', 50, 210, 'первая строка')]
c.executemany("INSERT INTO t (name, num, r, no) VALUES (?,?,?,?)", t_9)
conn.commit()
# Нарушений нет. Мы не передаём поле i и по ограничению оно принимает по умолчанию значение 100000

# Набор значений 10
t_10 = [('aabbff', 500000, 210, 'первая строка')]
c.executemany("INSERT INTO t (name, i, r, no) VALUES (?,?,?,?)", t_10)
conn.commit()
# Нарушений нет

# Набор значений 11
# t_11 = [('aabbff', 500000, 210)]
# c.executemany("INSERT INTO t (name, i, r) VALUES (?,?,?)", t_11)
# conn.commit()
# Нарушено ограничение NOT NULL no 


# Задание 2
c.execute('''CREATE TABLE IF NOT EXISTS Customers (
    Id INT CONSTRAINT PK_Customer_Id PRIMARY KEY,
    Age INT
        CONSTRAINT DF_Customer_Age DEFAULT 18 
        CONSTRAINT CK_Customer_Age CHECK(Age >0 AND Age < 100),
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Email VARCHAR(30) CONSTRAINT UQ_Customer_Email UNIQUE,
    Phone VARCHAR(20) CONSTRAINT UQ_Customer_Phone UNIQUE)''')

# Набор значений 1
# Customers_1 = [(1, 25, 'Иван', 'Петров', 't@mail.ru', '111-11-11'),
#         (1, 26, 'Василий', 'Васильев', 'v@mail.ru', '111-22-22')]
# c.executemany("INSERT INTO Customers (id, Age, FirstName, LastName, Email, Phone) VALUES (?,?,?,?,?,?)", Customers_1)
# conn.commit()
# Нарушено ограничение UNIQUE id

# Набор значений 2
# Customers_2 = [(1, 100, 'Иван', 'Петров', 't@mail.ru', '111-11-11')]
# c.executemany("INSERT INTO Customers (id, Age, FirstName, LastName, Email, Phone) VALUES (?,?,?,?,?,?)", Customers_2)
# conn.commit()
# Нарушено ограничение CHECK CK_Customer_Age

# Набор значений 3
# Customers_3 = [(2, 'Иван', 'Петров', 't@mail.ru', '111-11-11')]
# c.executemany("INSERT INTO Customers (id, FirstName, LastName, Email, Phone) VALUES (?,?,?,?,?)", Customers_3)
# conn.commit()
# Нарушений нет. Мы не передаём поле Age и DF_Customer_Age DEFAULT 18 по умолчанию присваивает значение 18

# Набор значений 4
# Customers_4 = [(1, 25, 'Иван', 'Петров', 't@mail.ru', '111-11-11'),
#         (2, 26, 'Василий', 'Васильев', 't@mail.ru', '111-22-22')]
# c.executemany("INSERT INTO Customers (id, Age, FirstName, LastName, Email, Phone) VALUES (?,?,?,?,?,?)", Customers_4)
# conn.commit()
# Нарушено ограничение UNIQUE Email

# Набор значений 5
# Customers_5 = [(1, 25, 'Иван', 'Петров', 't@mail.ru', '111-11-11'),
#         (2, 26, 'Василий', 'Васильев', 'v@mail.ru', '111-11-11')]
# c.executemany("INSERT INTO Customers (id, Age, FirstName, LastName, Email, Phone) VALUES (?,?,?,?,?,?)", Customers_5)
# conn.commit()
# Нарушено ограничение UNIQUE Phone

# Набор значений 6
# Customers_6 = [(1, 25, 'Петров', 't@mail.ru', '111-11-11')]
# c.executemany("INSERT INTO Customers (id, Age, LastName, Email, Phone) VALUES (?,?,?,?,?)", Customers_6)
# conn.commit()
# Нарушено ограничение NOT NULL FirstName

# Набор значений 7
# Customers_7 = [(1, 25, 'Иван', 't@mail.ru', '111-11-11')]
# c.executemany("INSERT INTO Customers (id, Age, FirstName, Email, Phone) VALUES (?,?,?,?,?)", Customers_7)
# conn.commit()
# Нарушено ограничение NOT NULL LastName

# Набор значений 8
Customers_8 = [(25, 'Иван', 'Петров', 't@mail.ru', '111-11-11')]
c.executemany("INSERT INTO Customers (Age, FirstName, LastName, Email, Phone) VALUES (?,?,?,?,?)", Customers_8)
conn.commit()
# Нарушений нет


# Задание 3
# Создание таблицы job_title
c.execute('''CREATE TABLE IF NOT EXISTS job_titles (
title VARCHAR(25) NOT NULL CONSTRAINT PK_title PRIMARY KEY,
salary REAL NOT NULL
        CONSTRAINT CK_salary CHECK (salary > 0))''')

# Создание таблицы experience
c.execute('''create table IF NOT EXISTS experience (
exp INT(2) NOT NULL
        CONSTRAINT PK_exp PRIMARY KEY
        CONSTRAINT CK_exp CHECK (exp > 0),
bonus INT(10) NOT NULL)''')

# Создание таблицы teachers
c.execute('''CREATE TABLE IF NOT EXISTS teachers (
name VARCHAR(50) NOT NULL CONSTRAINT PK_name PRIMARY KEY,
title VARCHAR(25) NOT NULL,
exp INT(2) NOT NULL,
department VARCHAR(10) NOT NULL
        CONSTRAINT DF_department DEFAULT 200,
FOREIGN KEY (title) REFERENCES job_titles (title),
FOREIGN KEY (exp) REFERENCES experience (exp))''')

# Создание таблицы teachers_class
c.execute('''CREATE TABLE IF NOT EXISTS teachers_class (
name VARCHAR(50) NOT NULL,
topic VARCHAR(25) NOT NULL ,
class VARCHAR(7) NOT NULL ,
type_lesson VARCHAR(10) NOT NULL,
PRIMARY KEY (name, topic, class),
FOREIGN KEY (name) REFERENCES teachers (name))''')


# Вывод содержимого таблиц
c.execute('''Select * from t''')
pp.pprint(c.fetchall())
c.execute('''Select * from Customers''')
pp.pprint(c.fetchall())
c.execute('''Select * from job_titles''')
pp.pprint(c.fetchall())
c.execute('''Select * from experience''')
pp.pprint(c.fetchall())
c.execute('''Select * from teachers''')
pp.pprint(c.fetchall())
c.execute('''Select * from teachers_class''')
pp.pprint(c.fetchall())

# Закрытие передачи
conn.close() 