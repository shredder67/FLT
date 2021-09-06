from pathlib import Path
from lab6 import    sort_machine as expression_sort_machine, \
                    calc as calc_expression 

kw  =   {'&': 5, '|' : 4, '¬' : 6, '→' : 3, '↔' : 2, '(' : -1, ')' : -1,
        '<': 1, '>': 1, '=' : 1 }
flags = {'t': 1, 'f': 0}

# Описание логических операций конююкции, 
# дизъюнкции, инверсии, импликации, равносильности и скобок
# Значения задаются с помощью отношений между числами/выражениями
# или флагами t и f (соответственно true и false)
# Выражения просчитываются вызовами функций из предыдущей работы

def read(filename):
    str = list(open(filename, 'r', encoding='utf-8').read())
    return str

def next_op(str: list, index):
    while(str[index] not in kw and index < len(str)):
        index += 1
    return index

def sort_machine(str : list):
    op_stack = []
    res = []
    kw_list = list(kw.keys())
    flags_list = list(flags.keys())

    i = 0
    while(i < len(str)):
        if str[i] in kw_list:
            if str[i] == '(':
                op_stack.append(str[i])
            elif str[i] == ')':
                while op_stack[-1] != '(':
                    res.append(op_stack.pop())
                op_stack.pop()
            else: # операция
                while len(op_stack) > 0 and kw[op_stack[-1]] >= kw[str[i]]:
                        res.append(op_stack.pop())
                op_stack.append(str[i])
        else: # операнд
            if(str[i] in flags_list):
                res.append(bool(flags[str[i]]))
            else:
                # расчет арифметического выражения
                right_boundary = next_op(str, i)
                parsed_sequence = expression_sort_machine(str[i:right_boundary])
                res.append(calc_expression(parsed_sequence))
                i = right_boundary
                continue
        i += 1
    
    if op_stack:
        op_stack.reverse()
        res += op_stack  
    return res

def calc(str : list):
    res = []
    kw_list = kw.keys()
    for i in range(len(str)):
        if str[i] in kw_list:
            if str[i] == '¬':
                res[-1] = not res[-1]
            else:
                t2 = res.pop()
                t1 = res.pop()
                if str[i] == '&':
                    res.append(t1 and t2)
                elif str[i] == '|':
                    res.append(t1 or t2)
                elif str[i] == '→':
                    res.append(not t1 or t2)
                elif str[i] == '↔':
                    res.append(t1 == t2)
                elif str[i] == '>':
                    res.append(t1 > t2)
                elif str[i] == '<':
                    res.append(t1 < t2)
                elif str[i] == '=':
                    res.append(t1 == t2)
        else:
            res.append(int(str[i]))
    return res[0]

def main():
    str = Path('example_7.txt').read_text(encoding='utf8').replace(' ', '')

    rev_polish_notation= sort_machine(str)
    print(rev_polish_notation)

    res = calc(rev_polish_notation)
    print("Результат: ", res)

if __name__ == '__main__':
    main()