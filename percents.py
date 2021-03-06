"""
Задание

Дан набор из N долей, представленных в виде N рациональных.
Необходимо представить эти доли в процентном выражении c точностью до трех знаков после запятой.

Входные данные
Первая строка содержит значение N - число долей, каждая последующая содержит числовое выражение доли.
4
1.5
3
6
1.5

Выходные данные
N строк с процентным выражением долей.
Значение в строке k является процентным выражение доли из строки k+1 входных данных

0.125
0.250
0.500
0.125

Идея решения:
    1. Просуммировать все входящие значения, чтобы получить размер целого
    2. Рассчитать, какую долю в процентах от целого занимает каждое входящее значение из пункта 1

Пример запуска:
    python3 percents.py <путь до файла с входящими данными> <путь до файла, куда записать результат>
    python3 percents.py percents.txt percents_out.txt

Дополнительно:
    1.1 Оценка вычислительной сложности
        Вычислительная сложность алгоритма - линейная, O(n)

        Алгоритму необходимо произвести N преобразований входящих данных в объекты типа Decimal для вычислений с учетом
        заданной точности, произвести N сложений, чтобы получить сумму элементов и произвести N делений долей на сумму,
        чтобы получить процентную долю для каждого входящего значения.
        Сложность каждого шага линейная. N - число входящих элементов.
    1.2 Оценка необходимой памяти.
       Для решения необходимо загрузить в память N объектов типа Decimal (доли из входящих данных), постоянно хранить
       в памяти один объект типа Decimal с суммой входящих значений и один объект типа Decimal для хранения процентного
       выражения рассчитываемой в данный момент доли (после расчета процентного выражения доли значение отправляется
       в файл или буфер и не хранится отдельным объектов в памяти).

       Таким образом алгоритму потребуется (N + 2) * размер Decimal памяти, где N - число элементов во входных данных.
       Один объект Decimal занимает 104 байта.

       Стоит отметить, что для работы так же потребуются накладные расходы по памяти на работу с файлами
       (чтение и запись), которые подсчитать сложнее. Значительную часть из них составит хранение в буфере данных для
       файла с выходными данными. Они храняться в памяти до момента сохранения на диск, которое происходит один раз
       в самом конце. Можно производить запись на диск после каждого обработанного значения, что минимизирует затраты
       памяти на буфер, но увеличит время работы.
    2. Ограничение на размер входных параметров - входной файл формата txt 5 - 7 млн строк и размером до 100 Мб
       Скрипт отрабатывает за ~8 секунд при 5 млн строк (чисел с плавающей точкой) во входном файле размером 90 Мб.
       Конфигурация машины: 2,8 GHz 4‑ядерный процессор Intel Core i7, досточное кол-во памяти, SSD диски
    3. Субъективная оценка сложности - 1, затраченное время - 2 час (с оформлением и доп. заданиями)
"""
from decimal import Decimal, getcontext

getcontext().prec = 3


def convert_shares_to_percents(*shares):
    total = sum(shares)
    return (share / total for share in shares)


if __name__ == '__main__':
    import sys

    shares = []

    input_file_path = sys.argv[1]
    with open(input_file_path, 'r') as input_file:
        for row_number, row in enumerate(input_file, start=1):
            if row_number == 1:
                continue
            shares.append(Decimal(row.strip()))

    percents = convert_shares_to_percents(*shares)

    output_file_path = sys.argv[2]
    with open(output_file_path, 'w') as output_file:
        for value in percents:
            output_file.write(str(value) + '\n')
