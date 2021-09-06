import random
import main6 as alg_pn

# генерирует n-мерную матрицу с случайными значениями
def n_arr(i, l):
    if i == 1:
        return [random.randrange(0, 11) for _ in range(l)]
    else:
        return [n_arr(i - 1, l) for _ in range(l)]

# преобразует n-мерный массив в одномерный
def transform_n_to_one(i, source):
    res = []
    if i != 1:
        for row in source:
            res += transform_n_to_one(i - 1, row)
        return res
    else:
        for el in source:
            res.append(el)
        return res

# генерирует PN-запись для обращения к элементу массива
def sort_machine(n, l, arr, expr):  
    #подключаемый модуль main6 содержит необходимый функционал для парсинга арифметических выражений
    parsed_expr = alg_pn.sort_machine(list(expr))
    return parsed_expr

# вычисляет непосредственно индекс ячейки памяти по полученной формуле в PN
def calc(str : list):
    res = alg_pn.calc(str)
    return res


# генерирует строку с формулой для индекса в одномерном массиве
def generate_formula(n, l, adresses : list):
    # adress = [i1, i2, ..., il]
    # в рассматриваемом примере все глубины в массиве имеют одинаковый порядок l
    def generate_suffix(n, l, adresses : list):
        if adresses:
            return ')*{}+{}'.format(l, adresses[0]) + generate_suffix(n, l, adresses[1:])
        return ''
    if n >= 2:
        return ('('*(n - 2)) + '{}*{}+{}'.format(adresses[0], l, adresses[1]) + generate_suffix(n, l, adresses[2:])
    else:
        # случай одномерного массива
        return str(adresses[0])

def main():
    n = int(input('Введите размерность массива: '))
    l = int(input('Введите длину в одном измерении: '))
    arr = n_arr(n, l)
    arr1 = transform_n_to_one(n, arr)


    print('Исходный массив\n-------\n',arr)
    print('\nСгенерированный одномерный\n-------\n',arr1)

    print('\nВведите адрес ячейки массива в формате "i1 i2 ... il"')

    adr = list(map(int, input().split()))
    expr = generate_formula(n, l, adr)
    sorted = sort_machine(n,l,arr, expr)
    print(sorted)
    res_adr = calc(sorted)
    print('Результат обращения:\narr w*[{}] = arr w*[{}] = {}'.format(expr, res_adr, arr1[res_adr]))


if __name__ == "__main__":
    main()