class Sword:
    def __init__(self, name, material, blade_length, grip):
        self.name = name
        self.blade_length = blade_length
        self.material = material
        self.grip = grip
        print(f'Новый меч {name} выкован!')

    def slashing_blow(self):
        return (f'Нанесён рубящий удар мечом {self.name}. '
                f'Радиус поражения: {self.blade_length}.')

    def piercing_strike(self):
        return (f'Нанесён пронзающий удар мечом {self.name}. '
                f'Рукоять {self.grip} мягко легла в руку.')

    def sharpen(self):
        return (f'Меч "{self.name}" заточен,'
                f' {self.material} отлично поддалась обработке.')

first_sword = Sword('Тренировочный',
                   'Кора железного дуба',
                   1.2, 'хват одной рукой')

print('Перед вами манекен, опробуйте удары на нём.')
print(first_sword.slashing_blow())
print(first_sword.piercing_strike())
print('Обслуженное оружие никогда не подведёт.')
print(first_sword.sharpen())