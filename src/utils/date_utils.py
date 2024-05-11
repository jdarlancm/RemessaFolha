from enum import Enum


class Meses(Enum):
    JAN = 1
    FEV = 2
    MAR = 3
    ABR = 4
    MAI = 5
    JUN = 6
    JUL = 7
    AGO = 8
    SET = 9
    OUT = 10
    NOV = 11
    DEZ = 12


def nome_mes(mes):
    return Meses(mes).name.lower()
