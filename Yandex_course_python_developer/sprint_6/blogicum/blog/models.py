from django.db import models

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать отложенные публикации.'
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор публикации')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, verbose_name='Местоположение')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

class Category(models.Model):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено',auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Location(models.Model):
    name = models.CharField('Название места',max_length=256)
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено',auto_now_add=True)

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'