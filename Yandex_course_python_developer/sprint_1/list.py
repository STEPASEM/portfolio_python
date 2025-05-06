movie_ratings = [4.7, 5.0, 4.3, 3.8]
new_movie_ratings = [
   rating + 0.2 if rating < 4.9 else rating for rating in movie_ratings
]
print(new_movie_ratings)
# Вывод в терминал: [4.9, 5.0, 4.5, 4.0]


movie_ratings = [4.7, 5.0, 4.3, 3.8]
new_movie_ratings = [rating for rating in movie_ratings if rating > 4.5]
print(new_movie_ratings)
# Вывод в терминал:[4.7, 5.0]


movie_ratings = [4.7, 5.0, 4.3, 3.8]
movies = ['Матрица', 'Хакеры', 'Трон']
print(id(movies))
# Вывод в терминал: 2217539360448
movies.extend(movie_ratings)
print(movies)
# Вывод в терминал: ['Матрица', 'Хакеры', 'Трон', 4.7, 5.0, 4.3, 3.8]
print(id(movies))
# Вывод в терминал: 2217539360448
# А при конкатенации в памяти будет создан новый объект, а не изменён существующий:
movies = movies + movie_ratings
print(movies)
# Вывод в терминал: ['Матрица', 'Хакеры', 'Трон', 4.7, 5.0, 4.3, 3.8]
print(id(movies))
# Вывод в терминал: 2217540656384
# Другой ID - другой объект.


movie_ratings = [4.7, 5.0, 4.3, 3.8, 4.7, 4.1]
print(id(movie_ratings))
# Вывод в терминал: 27337512
# Разворот списка методом reverse()
movie_ratings.reverse()
print(id(movie_ratings))
# Вывод в терминал: 27337512
print(movie_ratings)
# Вывод в терминал: [4.1, 4.7, 3.8, 4.3, 5.0, 4.7]

movie_ratings = [4.7, 5.0, 4.3, 3.8, 4.7, 4.1]
print(id(movie_ratings))
# Вывод в терминал: 2028420139712
# Разворот списка с помощью среза
movie_ratings = movie_ratings[::-1]
print(movie_ratings)
# Вывод в терминал: [4.1, 4.7, 3.8, 4.3, 5.0, 4.7]
# Список инвертирован, но...
print(id(movie_ratings))
# Вывод в терминал: 2028420159168
# Это уже другой объект!