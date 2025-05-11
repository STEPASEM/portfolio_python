
class Bird:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def describe(self, full=False):
        """Выводит информацию о птице."""
        return f'Размер птицы {self.name} - {self.size}.'


class Parrot(Bird):
    def __init__(self, name, size, color):
        super().__init__(name, size)
        self.color = color

    def describe(self, full=False):
        """Выводит информацию о попугае."""
        if full:
            return (f'Попугай {self.name} — заметная птица,'
                    f'окрас её перьев — {self.color}, а размер — {self.size}. '
                    f'Интересный факт: попугаи чувствуют ритм, а вовсе не бездумно'
                    f'двигаются под музыку. Если сменить композицию, то и темп движений птицы изменится.')
        return super().describe()

    def repeat(self, phrase):
        """Повторяет фразу."""
        return f'Попугай {self.name} говорит: {phrase}'


class Penguin(Bird):
    def __init__(self, name, size, genus):
        super().__init__(name, size)
        self.genus = genus

    def describe(self, full=False):
        """Выводит информацию о пингвине."""
        if full:
            return (f'Размер пингвина {self.name} из рода {self.genus} — {self.size}.'
                    f'Интересный факт: однажды группа геологов-разведчиков похитила'
                    f'пингвинье яйцо, и их принялась преследовать вся стая, не пытаясь,'
                    f'впрочем, при этом нападать. Посовещавшись, похитители вернули птицам яйцо, и те отстали.')
        return super().describe()

    def swimming(self):
        """Плавание пингвина."""
        return f'Пингвин {self.name} плавает со средней скоростью 11 км/ч.'


kesha = Parrot('Ара', 'средний', 'красный')
kowalski = Penguin('Королевский', 'большой', 'Aptenodytes')

print(kesha.repeat('Кеша хороший'))
print(kowalski.swimming())
