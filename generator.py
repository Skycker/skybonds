"""
Dummy generator of random values for scripts percents.py and trader.py
"""
import random

with open('percents_test.txt', 'w') as f:
    n = 5000000
    f.write(str(n) + '\n')
    for x in range(n):
        f.write(str(random.uniform(0, 100000)) + '\n')


with open('trader_test.txt', 'w') as f:
    n = 20
    f.write("{} {} {}\n".format(n, 1, 50000))
    for x in range(n):
        f.write("{} {} {} {}\n".format(x, 'bond-{}'.format(n), random.randint(90, 105), random.randint(1, 10)))


