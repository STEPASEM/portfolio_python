# Всем привет и это мои работы на python

## Папка internship
Содержит задачи, решаемые в рамках каких-то проектах, фриланса и просто личного интереса

## Папка Yandex_CodeRun
Содержит задачи, которые я решал в рамках Yandex_CodeRun

## Папка Yandex_course_python_developer
Содержит задачи, которые я решал проходя курс Python-разработчик от Яндекса.
Так же ниже расписал что было пройденно в каждом разделе.

#### sprint_1
* Основы Python

#### sprint_2
* venv и командная строка
* Git
* Правильное написание кода

#### sprint_3
* ООП

#### sprint_4
* Основы Django
    * acme_project - сайт по продаже мороженного
    * blogicum - сайт для ведения блога
        

        python manage.py startapp <name> -- создание приложения
        django-admin startproject <name> -- создание проекта
        python manage.py runserver -- запуск сервера

#### sprint_5
* Введение в базы данных


    winpty sqlite3 - подключение к sqlite3
    sqlite3 name.db - создание базы данных
    .mode table - вывод в виде таблицы
    <> — «не равно»
    BETWEEN начало_диапазона AND конец_диапазона
    IN — вхождение в список
    LIKE — поиск строки по шаблону
    LIMIT <сколько строк нужно показать> 
    OFFSET <на сколько строк сдвинуть выборку>
    COUNT() — количество строк в полученной выборке
    AVG («среднее») и SUM («сумма»)
    GROUP BY — найти «группы» объединённые одинаковым значением
                в заданной колонке
    HAVING - позволяет выполнить фильтрацию групп: она определяет,
              какие группы будут включены в результирующую выборку
    UNION — она объединяет данные из нескольких результирующих
            таблиц в одну
    ALTER TABLE - Изменение таблицы 

#### sprint_5
* Django ORM(модели и запросы)
* Создание админ зоны

Типы полей в Django

    models.IntegerField() — натуральное число (INTEGER);
    models.FloatField() — число с плавающей точкой (REAL);
    models.BooleanField() — булев тип False/True (BOOL);
    models.CharField() — строка (текстовое поле с ограничением
                          по числу символов) (VARCHAR);
    models.TextField() — текстовое поле (TEXT);
    models.DateField() — datetime.date в Python(DATE);
    models.DateTimeField() — дата и время, как datetime.datetime
                              в Python (DATATIME);
    models.SlugField() — «слаг», для строк, состоящих только из цифр
                          и букв латиницы и символов - и _. 
                          Обычно слаг используют для создания
                          коротких, человекочитаемых URL;
    models.ImageField() — для изображений.

Типы связей в Django

    models.OneToOneField() — один ко одному;
    models.ForeignKey() — многие к одному;
    models.ManyToManyField() — многие ко многим

Миграции В Django

    python manage.py makemigrations - создание миграций
    python manage.py migrate - применение миграций

Загрузка и выгрузка фикстур в/из БД

    python manage.py loaddata db.json - загрузка
    python manage.py dumpdata -o db.json  - выгрузка
    python manage.py dumpdata ice_cream -o ice_cream.json - выгрузка
                                              конкретного приложения
    python -Xutf8 <- чтобы не возникало проблем с кириллицей

Для перевода админки
    
    verbose_name - указывается в apps и получаем перевод приложения
    
    УКАЗЫВАЕМ В МОДЕЛЯХ:
    verbose_name — расширенное название модели
    verbose_name_plural — расширенное название во множественном числе

    ЕСЛИ ЗНАЧЕНИЕ КОРТЕЖА В АДМИНКЕ НЕТ ТО
    empty_value_display = '' - указываем на что заменяем прочерк