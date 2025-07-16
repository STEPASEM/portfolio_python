import sqlite3

con = sqlite3.connect('db.db')
cur = con.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS original_titles(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_types(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS video_products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    original_title_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    FOREIGN KEY(original_title_id) REFERENCES original_titles(id),
    FOREIGN KEY(type_id) REFERENCES product_types(id),
    UNIQUE(original_title_id)
);
''')

#ЗАПОЛНЕНИЕ ТАБЛИЦЫ
"""original_titles = [
    (1, 'Last Action Hero'),
    (2, 'Murder, She Wrote'),
    (3, 'Looney Tunes'),
    (4, 'Il Buono, il brutto, il cattivo'),
    (5, 'Who Framed Roger Rabbit'),
    (6, 'Merrie Melodies'),
    (7, 'Mrs. \'Arris Goes to Paris')
]

product_types = [
    (1, 'Мультфильм'),
    (2, 'Мультсериал'),
    (3, 'Фильм'),
    (4, 'Сериал'),
]

video_products = [
    (1, 'Безумные мелодии Луни Тюнз', 3, 2),
    (2, 'Весёлые мелодии', 6, 2),
    (3, 'Кто подставил кролика Роджера', 5, 3),
    (4, 'Хороший, плохой, злой', 4, 3),
    (5, 'Последний киногерой', 1, 3),
    (6, 'Она написала убийство', 2, 4),
    (7, 'Миссис Харрис едет в Париж', 7, 3)
]

cur.executemany('INSERT INTO original_titles VALUES(?, ?);', original_titles)
cur.executemany('INSERT INTO product_types VALUES(?, ?);', product_types)
cur.executemany('INSERT INTO video_products VALUES(?, ?, ?, ?);', video_products)

con.commit()"""


#Можно давать коротки названия с помощью AS вот пример: "SELECT video_products.title AS translation"
results = cur.execute('''
-- Вернуть поле title из таблицы video_products и поле title из original_titles
SELECT video_products.title,
       original_titles.title
-- ...из двух таблиц
FROM video_products,
     original_titles
-- Выводить только те значения полей, для которых верно условие
WHERE video_products.original_title_id = original_titles.id;
''')

for result in results:
    print(result)

print()

results = cur.execute('''
SELECT video_products.title,
       product_types.name
FROM video_products,
     product_types
WHERE video_products.type_id = product_types.id AND product_types.name = 'Фильм';
''')

for result in results:
    print(result)

con.close()