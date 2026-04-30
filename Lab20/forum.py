# Стандартный шаблон
import sqlite3 
import pprint 
pp = pprint.PrettyPrinter(indent=1, width=80, compact=False) 
# Открытие передачи
conn = sqlite3.connect('Lab20/forum.sqlite') 
c = conn.cursor() 

# Создание таблицы USERS с автоинкрементным первичным ключом
c.execute('''CREATE TABLE IF NOT EXISTS users (
id_user integer PRIMARY KEY,
name varchar (15), 
email varchar (20),
password varchar (7))''')

# Вставка нескольких строк в таблицу users методом курсора
users_m = [('sergey', 'sergey@mail.com', '1111'),
            ('sveta', 'sveta@mail.ru', '2222'),
            ('ivan', 'ivan@rambler.ru', '8888'),
            ('katy','katy@gcom','1423')]
c.executemany("INSERT INTO users (name, email, password)  VALUES (?,?,?)", users_m)
conn.commit()

# Создание таблицы topics с автоинкрементным первичным ключом.
c.execute('''create table IF NOT EXISTS topics 
(id_topic integer PRIMARY KEY,
topic_name varchar(100) NOT NULL,
id_author int (10) NOT NULL,
FOREIGN KEY (id_author) REFERENCES users (id_user))''')

# Вставка 4х строк в таблицу topics методом курсора
topics_m = [('books', '1'),
            ('tea', '2'),
            ('candies', '3'),
            ('leafs', '4')]
c.executemany("INSERT INTO topics (topic_name, id_author)  VALUES (?,?)", topics_m)
conn.commit()

# Создание таблицы posts
c.execute('''CREATE TABLE IF NOT EXISTS posts (
id_post integer PRIMARY KEY,
message varchar(50) NOT NULL,
id_author int (10) NOT NULL,
id_topic int (10) NOT NULL,
FOREIGN KEY (id_author) REFERENCES users (id_user),
FOREIGN KEY (id_topic) REFERENCES topics (id_topic))''')

# Заполняем таблицу posts
posts_m = [('Думаю, надо сделать так', 1, 2), 
('Хорошая идея', 1, 1), 
( 'Давайте обсудим', 2, 1), 
( 'Согласна', 4 , 3)]
c.executemany("INSERT INTO posts (message, id_author, id_topic)  VALUES (?,?,?)", posts_m)
conn.commit()

# Вывод содержимого таблиц
c.execute('''Select * from users''')
pp.pprint(c.fetchall())
c.execute('''Select * from topics''')
pp.pprint(c.fetchall())
c.execute('''Select * from posts''')
pp.pprint(c.fetchall())

# Задание
# c.execute("""SELECT 
#     t.topic_name AS "Название темы",
#     p.post_text AS "Текст сообщения",
#     u.username AS "Имя пользователя"
# FROM 
#     posts AS p
# JOIN 
#     users AS u ON p.user_id = u.user_id
# JOIN 
#     topics AS t ON p.topic_id = t.topic_id""")
# pp.pprint(c.fetchall())

# Закрытие передачи
conn.close() 



