import os
from os import path
import scipy.stats as stats
import numpy as np


def elementsCount(matrix):
    n = 0
    for arr in matrix:
        n += len(arr)
    return n


def concat(matrix):
    result = []
    for arr in matrix:
        for i in arr:
            result.append(i)

    return result


def mean(arr):
    return sum(arr) / len(arr)


# межгрупповая вариация
def SSA(matrix):
    gen_mean = mean(concat(matrix))

    result = 0
    for arr in matrix:
        result += len(arr) * (mean(arr) - gen_mean) ** 2

    return result


# внутригрупповая вариация
def SSW(matrix):
    result = 0
    for arr in matrix:
        arr_mean = mean(arr)
        for i in arr:
            result += (i - arr_mean) ** 2

    return result


# межгрупповая дисперсия
def MSA(matrix):
    return SSA(matrix) / getDFN(matrix)


# внутригрупповая дисперсия
def MSW(matrix):
    return SSW(matrix) / getDFD(matrix)


def getFishersCritery(matrix):
    return MSA(matrix) / MSW(matrix)


def getDFN(matrix):
    return len(matrix) - 1


def getDFD(matrix):
    return elementsCount(matrix) - len(matrix)


def getCriticalFishersCritery(pvalue, matrix):
    dfn = getDFN(matrix)
    dfd = getDFD(matrix)
    return stats.f.isf(pvalue, dfn, dfd)

def inputCountSplit(num, count):
    if num.isdigit():
        num = int(num)
        if num > 1 and num < count:
            return (0, num)
        else:
            return(1, f'Количество серий, на которое стоит разделить выборку должно быть больше 1 и меньше {count - 1}.')
    else:
        return (2, 'Количество серий, на которое стоит разделить выборку не удалось преобразовать ввод в число.')

def inputSignificanceLevel(num):
    if num.replace('.', '', 1).isdigit():
        num = float(num)
        if num > 0 and num < 1:
            return (0, num)
        else:
            return (1, 'Уровень значимости должен быть больше 0 и меньше 1.')
    else:
        return (2, 'Уровень значимости не удалось преобразовать в число.')


def normalizeFloat(num):
    return "{:4.3e}".format(num)

def open_file(filename):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        fileString = ''
        for s in f:
            fileString += s.strip()
        fileString = fileString.replace(',', '.').replace('\t', ' ').replace('\n', ' ')
        f.close()
        return (0, fileString)
    else:
        return (1, "Введите корректное имя файла")
    
def summary(fCritery, fCriticalCritery):
    output = f'{normalizeFloat(fCritery)} {">=" if fCritery >= fCriticalCritery else "<"} {normalizeFloat(fCriticalCritery)}'
    output += '\n'
    output +=  f'{"Систематическая погрешность присутствует." if fCritery >= fCriticalCritery else "Систематическая погрешность отсутствует."}' 
    return output

