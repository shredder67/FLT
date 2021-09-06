import re

kw = {'+' : 1, '-' : 1, '*' : 2, '/' : 2, '(' : -1, ')' : -1, '=': 0, ';' : -1}

def read(filename):
    str = list(open(filename, 'r').read())
    return str

def sort_machine(str:list):
    op_stack = []
    res = []
    kw_list = kw.keys()
    pattern = re.compile(r'=[.]*') # шаблон для сложного знака присваивания

    i = 0
    while i < len(str):
        if str[i] in kw_list:
            if str[i] == '(':
                op_stack.append(str[i])
            elif str[i] == ')':
                while op_stack[-1] != '(':
                    res.append(op_stack.pop())
                op_stack.pop()
            else: # если операция
                if str[i] in ['+', '-', '*', '/'] and str[i + 1] == '=': # +=, -=, /=, *=
                    op_stack += ['=', str[i]]
                    res.append(str[i - 1])
                    i += 2
                    continue
                while len(op_stack) > 0 and not pattern.match(op_stack[-1]) and kw[op_stack[-1]] >= kw[str[i]]:
                        res.append(op_stack.pop())
                op_stack.append(str[i])
        else:
            if i > 0 and str[i - 1] not in kw_list: # слияние цифр в одно число
                res[-1] += str[i]
            else:
                res.append(str[i])
        i += 1
    
    if op_stack:
        op_stack.reverse()
        res += op_stack  
    return res

def main():
    str = read('example_8.txt')
    res = sort_machine(str)
    print(res)
    print(''.join(res))

if __name__ == "__main__":
    main()
