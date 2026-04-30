# Стандартный шаблон
import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent = 1, width = 80, compact = False) 
# Открытие передачи
conn = sqlite3.connect('Lab21/BD_UCH.sqlite') 
c = conn.cursor() 

# Используем команду проверки внешних ключей
c.execute('''PRAGMA foreign_keys = 1''')

# Удаляем таблицы целиком, начиная с самых зависимых
# c.execute('''drop table if exists teachers_class''')
# c.execute('''drop table if exists teachers''')
# c.execute('''drop table if exists job_titles''')
# c.execute('''drop table if exists experience''')
# conn.commit()

# Удаление всех строк таблиц, начиная с самых зависимых
c.execute('''Delete from teachers_class''')
c.execute('''Delete from teachers''')
c.execute('''Delete from job_titles''')
c.execute('''Delete from experience''')
conn.commit()

# Создание таблицы job_title
c.execute('''CREATE TABLE IF NOT EXISTS job_titles (
title VARCHAR(25) NOT NULL,
salary REAL NOT NULL,
PRIMARY KEY (title)
)''')

# Создание таблицы experience
c.execute('''create table IF NOT EXISTS experience (
exp INT(2) NOT NULL,
bonus INT(10) NOT NULL,
PRIMARY KEY (exp)
)''')

# Создание таблицы teachers
c.execute('''CREATE TABLE IF NOT EXISTS teachers (
name VARCHAR(50) NOT NULL,
title VARCHAR(25) NOT NULL,
exp INT(2) NOT NULL,
department VARCHAR(10) NOT NULL,
PRIMARY KEY (name),
FOREIGN KEY (title) REFERENCES job_titles (title),
FOREIGN KEY (exp) REFERENCES experience (exp)
)''')

# Создание таблицы teachers_class
c.execute('''CREATE TABLE IF NOT EXISTS teachers_class (
name VARCHAR(50) NOT NULL,
topic VARCHAR(25) NOT NULL,
class VARCHAR(7) NOT NULL,
type_lesson VARCHAR(10) NOT NULL,
PRIMARY KEY (name, topic, class),
FOREIGN KEY (name) REFERENCES teachers (name)
)''')

# Вставка нескольких строк в таблицу job_titles
job_titles_m = [('Преподаватель', '500'),
            ('Старший преподаватель', '800')]
c.executemany("INSERT INTO job_titles (title, salary) VALUES (?,?)", job_titles_m)
conn.commit()

# Вставка нескольких строк в таблицу experience
experience_m = [('5', '1'),
            ('7', '100'),
            ('10', '150')]
c.executemany("INSERT INTO experience (exp, bonus) VALUES (?,?)", experience_m)
conn.commit()

# Вставка нескольких строк в таблицу teachers
teachers_m = [('Иванов И.М.', 'Преподаватель', '5', '25'),
            ('Петров М.И.', 'Старший преподаватель', '7', '25'),
            ('Сидоров Н.Г.', 'Преподаватель', '10', '25'),
            ('Егоров В.В.', 'Преподаватель', '5', '24')]
c.executemany("INSERT INTO teachers (name, title, exp, department) VALUES (?,?,?,?)", teachers_m)
conn.commit()

# Вставка нескольких строк в таблицу teachers_class
teachers_class_m = [('Иванов И.М.', 'СУБД', '256', 'Практика'),
            ('Иванов И.М.', 'ПЛ/1', '123', 'Практика'),
            ('Петров М.И.', 'СУБД', '256', 'Лекция'),
            ('Петров М.И.', 'Паскаль', '256', 'Практика'),
            ('Сидоров Н.Г.', 'ПЛ/1', '123', 'Лекция'),
            ('Сидоров Н.Г.', 'Паскаль', '256', 'Лекция'),
            ('Егоров В.В.', 'ПЭВМ', '244', 'Лекция')]
c.executemany("INSERT INTO teachers_class (name, topic, class, type_lesson) VALUES (?,?,?,?)", teachers_class_m)
conn.commit()

# Вывод содержимого таблиц
c.execute('''Select * from teachers_class''')
pp.pprint(c.fetchall())
c.execute('''Select * from teachers''')
pp.pprint(c.fetchall())
c.execute('''Select * from job_titles''')
pp.pprint(c.fetchall())
c.execute('''Select * from experience''')
pp.pprint(c.fetchall())

# 5.6 Напишите запрос: какую заработную плату получает каждый сотрудник кафедры 25, учитывая надбавку за стаж
# c.execute("""
# SELECT * FROM teachers
#           JOIN
#           JOIN
# WHERE department = '25'
# """)
# pp.pprint(c.fetchall())

# Закрытие передачи
conn.close() 