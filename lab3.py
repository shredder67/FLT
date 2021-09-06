

def print_table(table):
    print('------------------')
    for row in table:
        for el in row:
            print('{}\t'.format(el), end='')
        print()
    print('------------------')

#объединяет терминальные символы корректным образом
def input_correction(inp, nonterm):
    for row in inp:
        for el in row:




def main():
    fr = open('source.txt', 'r', encoding='utf-8')
    n = int(fr.readline())
    terminal = list(fr.readline() + ['+', '-', '*', '/', '(', ')', 'x'])
    prod_list = [[] for _ in range(n)] # Таблица с введенными продукциями
    for i in range(n):
        prod_list[i] = fr.readline()
    fr.close()
    print_table(prod_list)







if __name__ == "__main__":
    main()