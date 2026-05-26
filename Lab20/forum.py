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

# c.execute ("INSERT INTO users (name, email, password) VALUES ('sergey', 'sergey@mail.ru', '1111')")

# Вставка нескольких строк в таблицу users методом курсора
users_m = [('sergey', 'sergey@mail.com', '1111'),
           ('sveta', 'sveta@mail.ru', '2222'),
           ('ivan', 'ivan@rambler.ru', '8888'),
           ('katy','katy@gcom','1423')]
c.executemany("INSERT INTO users (name, email, password)  VALUES (?, ?, ?)", users_m)
conn.commit()

# Создание таблицы topics с автоинкрементным первичным ключом.
c.execute('''create table IF NOT EXISTS topics (
          id_topic integer PRIMARY KEY,
          topic_name varchar(100) NOT NULL,
          id_author int (10) NOT NULL,
            FOREIGN KEY (id_author) REFERENCES users (id_user))''')

# Вставка 4х строк в таблицу topics методом курсора
topics_m = [('books', '1'),
            ('tea', '2'),
            ('candies', '3'),
            ('leafs', '4')]
c.executemany("INSERT INTO topics (topic_name, id_author)  VALUES (?, ?)", topics_m)
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
c.executemany("INSERT INTO posts (message, id_author, id_topic)  VALUES (?, ?, ?)", posts_m)
conn.commit()

# 3.4, 3.5 Вывод содержимого таблиц
c.execute('''Select * from users''')
pp.pprint(c.fetchall())
c.execute('''Select * from topics''')
pp.pprint(c.fetchall())
c.execute('''Select * from posts''')
pp.pprint(c.fetchall())

# 3.6
c.execute("""
          SELECT t.topic_name AS "Название темы", p.message AS "Текст сообщения", u.name AS "Имя пользователя"
          FROM posts AS p
            LEFT JOIN users AS u ON p.id_author = u.id_user
                JOIN topics AS t ON p.id_topic = t.id_topic
          """)
pp.pprint(c.fetchall())

# 3.7
c.execute("""
          SELECT t.topic_name AS "Название темы", u.name AS "Имя пользователя", p.message AS "Текст сообщения"
          FROM posts AS p
            JOIN topics AS t ON p.id_topic = t.id_topic
                JOIN users AS u ON t.id_author = u.id_user
          """)
pp.pprint(c.fetchall())

# 3.8
c.execute("""
          SELECT t.topic_name AS "Название темы", u_topic.name AS "Автор темы", p.message AS "Сообщение", u_post.name AS "Автор сообщения" 
          FROM posts p
            JOIN topics AS t ON p.id_topic = t.id_topic
                JOIN users AS u_topic ON t.id_author = u_topic.id_user
                    JOIN users AS u_post ON p.id_author = u_post.id_user;
          """)
pp.pprint(c.fetchall())

# 3.9
c.execute("""
          SELECT u.name AS "Имя пользователя", COUNT(t.id_topic) AS "Число тем"
          FROM users AS u
            LEFT JOIN topics AS t ON u.id_user = t.id_author
          GROUP BY u.id_user, u.name;
          """)
pp.pprint(c.fetchall())

# 3.10
c.execute("""
          SELECT u.name AS "Имя пользователя", COUNT(p.id_post) AS "Число сообщений"
          FROM users AS u
            LEFT JOIN posts AS p ON u.id_user = p.id_author
          GROUP BY u.id_user, u.name;
          """)
pp.pprint(c.fetchall())

# 3.11
c.execute("""
          SELECT u.name AS "Имя пользователя",
            (SELECT COUNT(*) FROM topics t WHERE t.id_author = u.id_user) AS "Число тем",
                (SELECT COUNT(*) FROM posts p WHERE p.id_author = u.id_user) AS "Число сообщений"
          FROM users AS u
          """)
pp.pprint(c.fetchall())

# c.execute('''Select name, sql from sqlite_master where type="table"''')
# pp.pprint(c.fetchall())

# Закрытие передачи
conn.close() 



