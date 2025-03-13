"""
Ссылка: https://coderun.yandex.ru/problem/median-out-of-three

Тип: Легкая

Раздел: Бекенд

Рассмотрим три числа a, b и c. Упорядочим их по возрастанию.
Какое число будет стоять между двумя другими?
"""
def main():
    a_b_c = list(map(int, input().split()))
    print(sorted(a_b_c)[1])

if __name__ == '__main__':
    main()