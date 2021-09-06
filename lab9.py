# Программа транслирует запись с условным операторами в обратную польскую
# В качестве примера в данной программе для выражений используются односимвольные литералы

kw = {'if' : -1, 'else' : -1, ':' : -1}

def read(filename):
    str = list(''.join(open(filename, 'r').read().split())) # удаляем все \t, \n и ' '
    return str

# Преобразует формулу в строку
def sort_station(str : list):
    op_stack = []
    res = []
    kw_list = kw.keys()
    label_stack = [] #стек меток {индекс метки: адрес позиции}

    str = parse_kw(str)
    print(str)
    for i in range(len(str)):
        if str[i] in kw_list:
            if str[i] in ['if', 'else']:
                op_stack.append(str[i])
            elif str[i] == ':':
                # В данном случае других операций, кроме if и else, нет
                # while op_stack[-1] not in ['if', 'else']:
                #    res.append(op_stack.pop())
                prev = op_stack.pop()

                #вставка метки перед оператором 
                res.append('[{}]'.format(len(label_stack)))
                label_stack.append(len(res) - 1) #адрес метки

                if prev == 'if':
                    res.append('!F')
                else:
                    res.append('!!')
                    # задать адрес для предыдущей метки
                    res[label_stack[len(label_stack) - 2]] = '(k + {})'.format(i + 1)
                    del label_stack[len(label_stack) - 2]        
        else:
            res.append(str[i])

    res.append(' ')

    #переход в конец строки при наличии неотмеченной метки
    if label_stack:
        res[label_stack[len(label_stack) - 1]] = '(k + {})'.format(len(res) - 1)

    #Все операции (if, else, :) уже были учтены   
    #if op_stack:
    #    op_stack.reverse()
    #    res += op_stack  
    return res

#объединяет символы в лексемы
def parse_kw(str : list):
    i = 0
    while i < len(str):
        if str[i] == 'i' and str[i + 1] == 'f':
            str[i] = 'if'
            del str[i + 1]
        elif str[i] == 'e' and str[i + 1] == 'l' and str[i + 2] == 's' and str[i + 3] == 'e':
            str[i] = 'else'
            del str[i + 1 : i + 4]
        i += 1
    return str

def main():
    # чтение даннных для примера и разбиение на лекс. единицы
    str = read('example_9.txt')
    str = parse_kw(str)
    str = sort_station(str)
    print(str)

if __name__ == "__main__":
    main()