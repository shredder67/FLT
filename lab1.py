
class NKA:
    # 1 Пример для тестов, соотв. регулярному выражению (a|b)*abb
    # '`' соответствует символу пустой строки

    # __s_state = 0
    # __f_states = set([3])
    # __alph = ['a', 'b']
    # __transition_table = [
    #     {'a': [0, 1], 'b': [0], '`': []},
    #     {'a': [], 'b': [2], '`': []},
    #     {'a': [], 'b': [3], '`': []},
    #     {'a': [], 'b': [], '`': []},
    # ]

    # 2 Пример для тестов, соотв. регулярному выражению (a|b)*abb
    # '`' соответствует символу пустой строки

    __s_state = 0
    __f_states = set([10])
    __alph = ['a', 'b']
    __transition_table = [
        {'a': [], 'b': [], '`': [1, 7]},
        {'a': [], 'b': [], '`': [2, 4]},
        {'a': [3], 'b': [], '`': []},
        {'a': [], 'b': [], '`': [6]},
        {'a': [], 'b': [5], '`': []},
        {'a': [], 'b': [], '`': [6]},
        {'a': [], 'b': [], '`': [1, 7]},
        {'a': [8], 'b': [], '`': []},
        {'a': [], 'b': [9], '`': []},
        {'a': [], 'b': [10], '`': []},
        {'a': [], 'b': [10], '`': []},
    ]

    def __init__(self):
        pass

    def __str__(self):
        res = ''
        t_alph = self.__alph.copy()
        t_alph.append('`')
        for symb in t_alph:
            res += '\t{}'.format(symb)
        res += '\n'
        
        for i in range(len(self.__transition_table)):
            res += '{}:'.format(i)
            for symb in t_alph:
                res += '\t{}'.format((self.__transition_table[i][symb] if self.__transition_table[i][symb] else '-'))
            res += '\n'
        res += 'Конечные состояния:{}'.format(self.__f_states)
        return res
    
    #Ввод НКА с консоли
    def input(self):
        s = int(input('Введите кол-во состояний НКА: '))
        n = int(input('Введите кол-во символов в алфавите: '))
        print("Введите все символы алфавита")
        alph = []
        for _ in range(n):
            alph.append(input())
        self.__alph = alph
        t_alph = self.__alph.copy()
        t_alph.append('`') 
        self.__f_states = list(map(int, input('Введите конечные состояния через пробел: ').split(' ')))
        print('Введите функции переходов для каждого символа у каждого состояния'
            '\nМножество переходов вводить через запятую, а в случае отсутствия -1')
        NKA = [{} for _ in range(s)]
        for i in range(s):
            print('\nПереходы из ', i, ' состояния\n---')
            for j in range(n + 1):
                inp = list(map(int, input('{}: '.format(t_alph[j])).split(', ')))
                if(inp != [-1]):
                    NKA[i][t_alph[j]] = inp
                else:
                    NKA[i][t_alph[j]] = []
        self.__transition_table = NKA

    def getFState(self):
        return  self.__f_states

    def getSState(self):
        return self.__s_state
    
    def getAlph(self):
        return self.__alph

    def getTransitionTable(self):
        return self.__transition_table

    #Возвращает множество состояний, достижимых из данного по e-переходам
    def e_closure_S(self, s : int):
        res = [s]
        for st in self.__transition_table[s]['`']:
            res += self.e_closure_S(st)
        return res

    #Возвращает множество состояний, достижимых из данных по e-переходам
    def e_closure_T(self, T : list):
        res = []
        for st in T:
            res += self.e_closure_S(st)
        return res

    #Возвращает множество состояний НКА, в которые имеется переход из данных при символе symb
    def move_T(self, T : list, symb : str):
        res = []
        for st1 in T:
            for st2 in self.__transition_table[st1][symb]:
                res.append(st2)
        return res

class DKA:
    __state = 0
    __f_states = set()
    __s_state = 0
    __alph = []
    __transition_table = []

    def __init__(self, nka):
        if(isinstance(nka, NKA)):
            self.cast_nka_to_dka(nka)
        else:
            raise ValueError('Wrong argument type!', type(nka))

    def __str__(self):
        res = ''
        for symb in self.__alph:
            res += '\t{}'.format(symb)
        res += '\n'
        for i in range(len(self.__transition_table)):
            res += '{}:'.format(i)
            for symb in self.__alph:
                res += '\t{}'.format((self.__transition_table[i][symb] if self.__transition_table[i][symb] else '-'))
            res += '\n'
        res += 'Конечные состояния:{}'.format(self.__f_states)
        return res

    #Преобразование данного НКА (или НКА-e) в ДКА
    def cast_nka_to_dka(self, nka : NKA):
        self.__alph = nka.getAlph()
        self.__s_state = nka.getSState()
        nka_F_states = set(nka.getFState())
        self._state = self.__s_state
        Dtran = [[], []]
        # словарь, переводящий номер состояния ДКА в множество состояний НКА
        # также содержит метки состояний (критерий завершенности ДКА)
        Dtran[0].append(set(nka.e_closure_S(self._state)))
        Dtran[1].append(False)
        # пока остаются непомеченные состояния
        flag = True
        while flag:
            flag = False
            for i in range(len(Dtran[1])):
                if not Dtran[1][i]: # если есть непомеченное состояние
                    Dtran[1][i] = True
                    self.__transition_table.append({})
                    flag = True
                    for symb in self.__alph: # Рассматриваем переход для каждого символа 
                        U = set(nka.e_closure_T(nka.move_T(list(Dtran[0][i]), symb))) # множество вершин, достижимых из рассматриваемой по символу symb
                        if U: # если не пустое множество (то есть существуют переходы)
                            if(U not in Dtran[0]):
                                Dtran[0].append(U)
                                Dtran[1].append(False)
                            self.__transition_table[i][symb] = Dtran[0].index(U)
                            fstates = (U & nka_F_states)
                            if fstates and (i + 1) not in self.__f_states and i + 1 < len(Dtran[1]):
                                self.__f_states.add(i + 1)

    #Применяет автомат к входной строке
    def apply(self, str):
        self.__state = 0
        symb = list(str)
        for i in range(len(symb)):
            self.__state = self.move(symb[i])
        if(self.__state in self.__f_states):
            return True
        return False

    #Переключение в след состояние
    def move(self, symbol):
        if(self.__transition_table[self.__state][symbol] is None):
            return self.__state
        return self.__transition_table[self.__state][symbol]

#Главная функция, содержит все необходимые вызовы
def main():
    # Пример выполнения и несколько тестовых прогонов для данных из примеры (см. комментарии в классе NKA)
    nka = NKA()
    print('Данный НКА:\n', nka)
    dka = DKA(nka)
    print('Полученный ДКА:\n', dka)
    print('Проверка строки "ababababababb": ', dka.apply('ababababababb'))
    print('Проверка строки "abb": ', dka.apply('abb'))
    print('Проверка строки "abababa": ', dka.apply('abababa'))

    # Для ввода собственного автомата раскоментируйте эти строки
    # nka = NKA()
    # nka.input()
    # dka = DKA(nka)

    # Для тестовых прогонов используйте функцию dka.apply(arg), где arg - входная строка

if __name__ == "__main__":
    main()