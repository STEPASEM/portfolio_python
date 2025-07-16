import sqlite3

con = sqlite3.connect("db_video.db")
con = con.cursor()

# ORDER BY сортировка
# ASC (по возрастанию) или DESC (по убыванию).

result = con.execute('''
    SELECT product_type,
           title,
           release_year
    FROM video_products
    WHERE release_year > 1980
    ORDER BY product_type DESC, title
    LIMIT 2 OFFSET 2;
''')

for res in result:
    print(res)
print()

res_dis = con.execute('''
    SELECT product_type,
       COUNT(*)
    FROM video_products
    GROUP BY product_type; 
''')

for res in res_dis:
    print(res)

con.close()