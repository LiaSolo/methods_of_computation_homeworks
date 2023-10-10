from math import sin
from prettytable import PrettyTable


def f(x_):
    return sin(x_) - x_**2/2


# x_ - что подставляем, x_k - что выкидываем
def l_kn(x_k, x_):
    w = w_dw(n+1, x_, x_k)
    dw = w_dw(n+1, x_k, x_k)
    return w/dw


def lagrange_polynom(n_, x_):
    ans = 0
    for x_k in selected_nodes[:n_+1]:
        ans += l_kn(x_k, x_) * all_nodes_table_dict[x_k]
    return ans


# k - до какой степени-1 идем, x_ - что подставляем, x_j - что выкидываем
def w_dw(k, x_, x_j):
    ans = 1
    for x_i in selected_nodes[:k]:
        if x_i != x_j:
            ans *= (x_ - x_i)
    return ans


#  n - степень-1 многочлена, x_ - что подставляем
def newton_polynom(k, x_):
    if k == 0:
        return A_k(0)
    ans = A_k(k)
    for i in range(k):
        x_i = selected_nodes[i]
        ans *= (x_ - x_i)
    return newton_polynom(k-1, x_) + ans


def A_k(k):
    ans = 0
    for j in range(k+1):
        x_j = selected_nodes[j]
        dw = w_dw(k+1, x_j, x_j)
        ans += all_nodes_table_dict[x_j]/dw
    return ans


# получаю n+1 узел, которые близко к заданному x_
def get_nodes_we_need(x_, n):
    nodes_we_need = []
    # сортирую в порядке отдаления x_i от x
    razn_temp = set()
    temp_dict = {}
    for node in nodes:
        razn = abs(x_ - node)
        razn_temp.add(razn)
        if razn in temp_dict.keys():
            temp_dict[razn].append(node)
        else:
            temp_dict[razn] = [node]
    razn_temp = list(razn_temp)
    razn_temp.sort()
    for t in razn_temp:
        for node in temp_dict[t]:
            nodes_we_need.append(node)
    return nodes_we_need[:n + 1]


def print_table(rows_list):
    table = PrettyTable(['i', 'X_i', 'f(X_i)'])
    i = 1
    for key in rows_list:
        table.add_row([i, key, all_nodes_table_dict[key]])
        i += 1
    print(table)


print('Задача алгебраического интерполирования')
print('Вариант 1')
print('Используются равноотстоящие узлы')
a, b = map(float, input('Введите через пробел начало и конец отрезка:').split())
m = int(input('Введите m, где m+1 - число значений в таблице:'))

h = (b - a)/m
nodes = [a + i*h for i in range(m + 1)]
all_nodes_table_dict = {x: f(x) for x in nodes}
print("Исходная таблица узел-значение")
print_table(nodes)

while True:
    n = int(input(f'Введите n - максимальную степень интерполяционного многочлена, n<={m}:'))
    while n > m:
        print('Некорректное значение n!')
        n = int(input(f'Введите n - максимальную степень интерполяционного многочлена, n<={m}:'))

    x = float(input('Введите, в какой точке посчитать функцию:'))
    selected_nodes = get_nodes_we_need(x, n)
    print("Отсортированная в порядке отдаления от x таблица узел-значение")
    print_table(selected_nodes)
    L_x = lagrange_polynom(n, x)
    print(f'Значение полинома Лагранжа L(x) в точке х = {x}:', L_x)
    print('Абсолютная фактическая погрешность |f(x)-L(x)| =', abs(f(x) - L_x))
    P_x = newton_polynom(n, x)
    print(f'Значение полинома Ньютона P(x) в точке х = {x}:', P_x)
    print('Абсолютная фактическая погрешность |f(x)-P(x)| =', abs(f(x) - P_x))
    flag = input('Хотите ввести новые значения? (y/n):')
    if flag == 'n':
        break
