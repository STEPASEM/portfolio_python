"""
Тип: Легкая

Задан массив a размера n. Необходимо посчитать количество уникальных элементов
в данном массиве. Элемент называется уникальным, если встречается в массиве ровно один раз.
"""

def main():
    len_list = int(input()) #нужно для задания
    array = list(map(int, input().split()))
    dict_ = {}
    for i in array:
        if i in dict_:
            dict_[i] += 1
        else:
            dict_[i] = 1
    print(len([num for num in array if dict_[num] == 1]))

if __name__ == '__main__':
    main()