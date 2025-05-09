from datetime import datetime as dt
import time


class Quest:

    def __init__(self, name, goal, description):
        self.name = name
        self.goal = goal
        self.description = description
        self.start_time = None
        self.end_time = None

    def accept_quest(self):
        if self.end_time:
            return 'С этим испытанием вы уже справились.'
        self.start_time = dt.now()
        return f'Начало {self.name} положено.'

    def pass_quest(self):
        if not self.start_time:
            return 'Нельзя завершить то, что не имеет начала!'
        self.end_time = dt.now()
        completion_time = self.end_time - self.start_time
        return f'Квест "{self.name}" окончен. Время выполнения квеста: {completion_time}'

    def __str__(self):
        if self.end_time:
            return f'Цель квеста {self.name} - {self.goal}. Квест завершён.'
        if self.start_time:
            return f'Цель квеста {self.name} - {self.goal}. Квест выполняется.'
        return f'Цель квеста {self.name} - {self.goal}.'


quest_name = 'Сбор пиксельники'
quest_goal = 'Соберите 12 ягод пиксельники.'
quest_description = '''
В древнем лесу Кодоборье растёт ягода "пиксельника".
Она нужна для приготовления целебных снадобий.
Соберите 12 ягод пиксельники.'''

new_quest = Quest(quest_name, quest_goal, quest_description)

print(new_quest.pass_quest())
print(new_quest.accept_quest())

time.sleep(3)

print(new_quest.pass_quest())
print(new_quest.accept_quest())

print(new_quest)