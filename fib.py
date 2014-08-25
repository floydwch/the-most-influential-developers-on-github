# -*- coding: utf-8 -*-

from math import sqrt


sqrt5 = sqrt(5)


def fib(n):
    return int(((1 + sqrt5) ** n - (1 - sqrt5) ** n) / (2 ** n * sqrt5))
