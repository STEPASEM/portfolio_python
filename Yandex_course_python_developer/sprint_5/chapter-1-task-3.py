import sqlite3
con = sqlite3.connect('db_video_type_slogan.db')
cur = con.cursor()

#ПРИМЕР ЗАПРОСА JOIN
results = cur.execute('''
    SELECT video_products.title,
           slogans.slogan_text,
           product_types.title
    FROM video_products
    JOIN slogans ON video_products.slogan_id = slogans.id
    JOIN product_types ON video_products.type_id = product_types.id; 
''')

#ПРИМЕР ЗАПРОСА LEFT JOIN
results = cur.execute('''
    SELECT video_products.title,
           slogans.slogan_text
    FROM video_products
    LEFT JOIN slogans ON video_products.slogan_id = slogans.id; 
''')

#ПРИМЕР ЗАПРОСА RIGHT JOIN
results = cur.execute('''
    SELECT video_products.title,
           product_types.title
    FROM video_products
    RIGHT JOIN product_types ON video_products.type_id = product_types.id; 
''')

#ПРИМЕР ЗАПРОСА FULL JOIN
results = cur.execute('''
    SELECT video_products.title,
           slogans.slogan_text
    FROM video_products
    FULL JOIN slogans ON video_products.slogan_id = slogans.id; 
''')

#ПРИМЕР ЗАПРОСА CROSS JOIN - декартово произведение
results = cur.execute('''
    SELECT video_products.title,
           slogans.slogan_text
    FROM video_products
    CROSS JOIN slogans; 
''')


"""
Переименование таблицы:
ALTER TABLE <имя таблицы>
RENAME TO <новое имя таблицы>; 

Добавление колонки:
ALTER TABLE <название таблицы> 
ADD COLUMN <имя колонки> <тип колонки>; 

Переименование колонки:
ALTER TABLE <название таблицы>
RENAME COLUMN <старое имя колонки>
TO <новое имя колонки>; 

Удаление колонки:
ALTER TABLE <название таблицы>
DROP COLUMN <имя колонки>

Команда для  удаления таблицы выглядит так:
DROP TABLE <имя таблицы>; 
"""

for result in results:
    print(result)

con.close()