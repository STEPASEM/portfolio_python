from datetime import date as da
from datetime import datetime

FORMAT = "%d.%m.%Y"

def get_days_to_birthday(date_birthday):
    today = da.today()
    birthday = da(today.year, date_birthday.month, date_birthday.day)
    days_left = (today - birthday).days
    if days_left < 0:
        days_left += 365
    return days_left

birthdays = [
    ('Лера', '16.05.2015'),
    ('Максим', '16.12.2011'),
    ('Толя','12.06.2016')
]

for name, date_birthday in birthdays:
    days_left = get_days_to_birthday(datetime.strptime(date_birthday, FORMAT))
    print(f'До {name} дней осталось: {days_left}')
