import main8 as alg_pn # арифметический парсинг + присваивание

# В данном примере логические выражения обозначаются однобуквенными заглавными литералами для упрощения
# символы операций, при преобразовании строки для унарного минуса используется символ _
kw = ['for', 'while', '(', ')', '{', '}', ';']

def read(filename):
    str = list(''.join(open(filename, 'r').read().split()))
    return str

def parse_kw(str : list):
    i = 0
    while i < len(str):
        if str[i] == 'w' and str[i + 1] == 'h' and str[i + 2] == 'i' and str[i + 3] == 'l' and str[i + 4] == 'e':
            str[i] = 'while'
            del str[i + 1 : i + 5]
        elif str[i] == 'f' and str[i + 1] == 'o' and str[i + 2] == 'r':
            str[i] = 'for'
            del str[i + 1 : i + 3]
        i += 1
    return str

def sort_machine(str : list):
    res = []
    label_stack = [] #стек меток {индекс метки: адрес позиции}

    str = parse_kw(str)
    print(str)
    i = 0
    while i < len(str):
        if str[i] in kw:
            if str[i] == 'for':
                #for является тернарным оператором, состоящим из двух алг. выражений и одной проверки с меткой
                parts = ''.join(str[i + 2 : str.index(')', i)]).split(';')
                res += alg_pn.sort_machine(list(parts[0]))
                res.append(parts[1])
                res.append('[{}]'.format(len(label_stack)))
                label_stack.append(len(res) - 1) #адрес метки
                res.append('!F')
                res += alg_pn.sort_machine(list(parts[2]))

                i = str.index(')', i)

            elif str[i] == 'while':
                res.append(str[i + 2])
                res.append('[{}]'.format(len(label_stack)))
                label_stack.append(len(res) - 1) #адрес метки
                res.append('!F')

                i += 3

            elif str[i] == '{':
                j = i + 1
                while str[j] != '}':
                    l = j
                    r = str.index(';', l)
                    res += alg_pn.sort_machine(str[l : r])
                    j = r + 1
                i = j
                res.append('(k + {})'.format(res.index('!F') - 2)) # метка возврата к логическому выражению
                res.append('!!')
                # задать адрес для предыдущей метки
                res[label_stack[len(label_stack) - 1]] = '(k + {})'.format(i)
                del label_stack[len(label_stack) - 1]
        i += 1

    res.append(' ')
    return res

def main():
    str = read('example_10_2.txt')
    sorted = sort_machine(str)
    print(sorted)

if __name__ == '__main__':
    main()