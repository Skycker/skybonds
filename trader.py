"""
Допустим, что на рынке существует некое множество облигаций с номиналом 1000 условных единиц,
по которым каждый день выплачивается купон размером 1 уе.
Погашение номинала облигации (то есть выплата 1000 условных единиц) происходит в конце срока.

Каждая облигация на рынке характеризуется названием (некая строка) и ценой,
цена выражается в виде процентов от номинала, то есть цена 98.5 соответствует цене 98,5% * 1000 = 985 условных единиц.

У некоего трейдера есть информация о том какие предложения по облигациям будут на рынке в ближайшие N дней.
По каждому дню он знает, какие лоты будут представлены на бирже: название облигации, цену и количество в штуках.
Каждый день на рынке может быть от 0 до M лотов. Трейдер располагает суммой денежных средств в количестве S.

Необходимо определить какие лоты в какие дни нужно купить, чтобы получить максимальный доход с учетом следующих условий:
1. Трейдер может только покупать облигации. Купленные облигации не продаются. 2.
   Трейдер может купить только весь лот целиком при наличии доступных денежных средств.
3. Выплаченные купоны по купленным облигациям не реинвестируются, то есть не увеличивают сумму доступных денежных средств.
4. Все купленные облигации будут погашены в день N+30.
5. Доход рассчитывается на день N+30, то есть после погашения облигаций.

Входные данные
На первой строке будут даны числа N, M и S.
Далее будет идти k строк вида “<день> <название облигации в виде строки без пробелов> <цена> <количество>”.
Ввод будет завершен пустой строкой.

2 2 8000
1 alfa-05 100.2 2
2 alfa-05 101.5 5
2 gazprom-17 100.0 2

В первой строке необходимо указать сумму дохода, полученного трейдером на день N+30.
В последующих строках привести купленные лоты в таком же формате, который используется во входных данных.
Последняя строка должна быть пустой.

135
2 alfa-05 101.5 5
2 gazprom-17 100.0 2

Идея решения:
    1. Разобрать входящие данные на доступные для покупки лоты
    2. Сформировать все возможные сочетания лотов из доступных для покупки.
       Сочетания могут быть разного размера, от 1 до n, где n - все доступные лоты.
       Для каждого сочетания можно рассчитать стоимость, доход и прибыль
    3. Отбросить сочетания, которые дороже, чем сумма располагаемых трейдером денежных средств
    4. Среди оставшихся сочетаний выбрать одно с максимальной прибыльностью

Пример запуска:
    python3 trader.py <путь до файла с входящими данными> <путь до файла, куда записать результат>
    python3 trader.py trader.txt trader_out.txt

Дополнительно:
    1.1 Оценка вычислительной сложности
        Идея решения строится на переборе всех возможных сочетаний из N входящих элементов.
        Причем могут быть выбраны комбинации различного размера: от 1 до N.
        Вспоминая из комбинаторики формулу количества сочетаний m элементов из множества в n элеметов,
        то фукнция для вычислительной сложности может быть выражена следующей формулой:
        https://share.getcloudapp.com/NQuDjeQD
        Рост меньше, чем O(n!), но все равно очень-очень быстрый
    1.2 Оценка необходимой памяти
        Каждая строка из строк входящего файла преобразовывается в кастомный тип данных - BondLot, требуется держать
        в памяти N объектов данного типа, где N - кол-во элементов во входящих данных. Так же требуется держать в памяти
        один объект типа BondLotSet для хранения лучшего набора облигаций и один объект этого же типа для хранения
        текущего набора, который сравнивается с лучшим на каждой итерации цикла.

        Таким образом алгоритму потребуется: N * size(BondLot) + 2 * size(BondLotSet) байт памяти.
        Для объекта типа BondLot необходимо 64 байта, для BondLotSet - тоже 64 байта.

        Как и в предудущей задаче будут сложно оцениваемые накладные расходы на работу с файлами и определение
        всевозможных сочетаний покупаемых облигаций. Так же потребуется память на хранение констант, списков и тд.
    2. Ограничение на размер входных параметров - входной файл формата txt 20 строк
       Скрипт отрабатывает за ~10 секунд при 20 облигациях во входном файле.
       Конфигурация машины: 2,8 GHz 4‑ядерный процессор Intel Core i7, досточное кол-во памяти, SSD диски
    3. Субъективная оценка сложности - 6, затраченное время - 8 часов (с оформлением и доп. заданиями)
"""
from itertools import combinations
from decimal import Decimal


class BondLot:
    _cost_per_one = None
    _cost = None
    _income = None
    _profit = None

    def __init__(self, buy_day_number, name, percent_cost, quantity, nominal, coupon_per_day, pay_day_number):
        self.buy_day_number = int(buy_day_number)
        self.name = name
        self.percent_cost = Decimal(percent_cost)
        self.quantity = int(quantity)
        self.nominal = Decimal(nominal)
        self.coupon_per_day = Decimal(coupon_per_day)
        self.pay_day_number = int(pay_day_number)

    @property
    def cost_per_one(self):
        """ Стоимость покупки одной облигации. """
        if not self._cost_per_one:
            self._cost_per_one = self.nominal * self.percent_cost / 100
        return self._cost_per_one

    @property
    def cost(self):
        """ Стоимость покупки лота. """
        if not self._cost:
            self._cost = self.quantity * self.cost_per_one
        return self._cost

    @property
    def income(self):
        """
        Доход от лота на день погашения облигации.
        Купон на день покупки не выплачивается.
        """
        if not self._income:
            income_per_one = self.nominal + self.coupon_per_day * (self.pay_day_number - self.buy_day_number)
            self._income = self.quantity * income_per_one
        return self._income

    @property
    def profit(self):
        """ Прибыль с лота на день погашения облигации. """
        if not self._profit:
            self._profit = self.income - self.cost
        return self._profit

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.buy_day_number, self.name, self.percent_cost, self.quantity)


class BondLotSet:
    _cost = None
    _profit = None

    def __init__(self, lots):
        self.lots = lots

    @property
    def cost(self):
        if not self._cost:
            self._cost = 0
            for lot in self.lots:
                self._cost += lot.cost
        return self._cost

    @property
    def profit(self):
        if not self._profit:
            self._profit = 0
            for lot in self.lots:
                self._profit += lot.profit
        return self._profit

    def __iter__(self):
        return iter(self.lots)


if __name__ == '__main__':
    import sys

    trade_days = None
    max_lots_number = None
    balance = None
    pay_day_number = None
    ownership_days = 30
    bond_nominal = 1000
    coupon = 1
    available_lots = []

    input_file_path = sys.argv[1]
    with open(input_file_path, 'r') as input_file:
        for row_number, row in enumerate(input_file, start=1):
            row_data = row.strip().split()
            if row_number == 1:
                trade_days = int(row_data[0])
                max_lots_number = int(row_data[1])
                balance = Decimal(row_data[2])
                pay_day_number = trade_days + ownership_days
            else:
                available_lots.append(
                    BondLot(
                        buy_day_number=row_data[0],
                        name=row_data[1],
                        percent_cost=row_data[2],
                        quantity=row_data[3],
                        nominal=bond_nominal,
                        coupon_per_day=coupon,
                        pay_day_number=pay_day_number
                    )
                )

    best_bond_set = None
    for combination_size in range(1, len(available_lots) + 1):
        for combination in combinations(available_lots, combination_size):
            bond_set = BondLotSet(lots=combination)
            if bond_set.cost > balance:
                continue
            if not best_bond_set or best_bond_set.profit < bond_set.profit:
                best_bond_set = bond_set

    output_file_path = sys.argv[2]
    with open(output_file_path, 'w') as output_file:
        if best_bond_set:
            output_file.write(str(best_bond_set.profit) + '\n')
            for lot in best_bond_set:
                output_file.write(str(lot) + '\n')
        else:
            # nothing bought - zero profit
            output_file.write("0\n")
