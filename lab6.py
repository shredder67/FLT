from pathlib import Path

# символы операций, при преобразовании строки (унарные знаки определяются во время выполения)
kw = {'+' : 1, '-' : 1, '*' : 2, '/' : 2, '(' : -1, ')' : -1}

def next_number(str, index) :
    res = ''
    while(index < len(str) and str[index] not in kw) :
        res += str[index]
        index += 1
    return res, index

def sort_machine(str : list):
    op_stack = []
    res = []
    kw_list = kw.keys()

    i = 0
    while(i < len(str)):
        if str[i] in kw_list:
            if str[i] == '(':
                op_stack.append(str[i])
            elif str[i] == ')':
                while op_stack[-1] != '(':
                    res.append(op_stack.pop())
                op_stack.pop()
            else: # если операция
                # проверка на унарный +/- (или любой другой знак, зависит от ввода)
                if (i == 0) or ((str[i - 1] in kw_list) and str[i - 1] != ')'):
                    str = str[:i] + '0' + str[i:] # вставка 0, превращение унарного знака в бинарный
                    continue
                else:
                    while len(op_stack) > 0 and kw[op_stack[-1]] >= kw[str[i]]:
                        res.append(op_stack.pop())
                    op_stack.append(str[i])
        else: # операнд
            num, ind = next_number(str, i) # чтение числа
            res.append(num) # запись числа со знаком
            i = ind
            continue
        i += 1
    
    if op_stack: # если остались операции в стеке
        op_stack.reverse()
        res += op_stack  
    return res

def calc(rp_notation : list):
    res = []
    kw_list = kw.keys()
    for i in range(len(rp_notation)):
        if rp_notation[i] in kw_list:
            t2 = res.pop()
            t1 = res.pop()
            if rp_notation[i] == '-':
                res.append(t1 - t2)
            elif rp_notation[i] == '+':
                res.append(t1 + t2)
            elif rp_notation[i] == '*':
                res.append(t1 * t2)
            elif rp_notation[i] == '/':
                res.append(t1 / t2)
        else:
            res.append(int(rp_notation[i]))
    return res[0]    

def main():
    str = Path('example_6.txt').read_text().replace(' ', '')
    print('Выражение:', str)
    rev_polish_notation = sort_machine(str)
    print(rev_polish_notation)
    result = calc(rev_polish_notation)
    print('Результат вычисления выражения:', result)

if __name__ == '__main__':
    main()