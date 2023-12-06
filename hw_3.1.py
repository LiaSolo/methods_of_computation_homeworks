from math import sin
from prettytable import PrettyTable


def f(x_):
    return sin(x_) - x_**2/2


def get_nodes_we_need(x_, n, nodes_or_revers):
    nodes_we_need = []
    # сортирую в порядке отдаления x_i от x
    razn_temp = set()
    temp_dict = {}
    for node in nodes_or_revers:
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


# k - до какой степени-1 идем, x_ - что подставляем, x_j - что выкидываем
def w_dw(k, x_, x_j, nodes_):
    ans = 1
    for x_i in nodes_[:k]:
        if x_i != x_j:
            ans *= (x_ - x_i)
    return ans


# x_ - что подставляем, x_k - что выкидываем
def l_kn(x_k, x_, nodes_):
    w = w_dw(n+1, x_, x_k, nodes_)
    dw = w_dw(n+1, x_k, x_k, nodes_)
    return w/dw


def lagrange_polynom(n_, x_, nodes_list, nodes_dict):
    ans = 0
    for x_k in nodes_list[:n_+1]:
        ans += l_kn(x_k, x_, nodes_list) * nodes_dict[x_k]
    return ans


def polynom(x_):
    if x_ in calculated_polynom_values:
        return calculated_polynom_values[x_]
    if x_ in all_nodes_table_dict:
        return all_nodes_table_dict[x_]

    nodes_ = get_nodes_we_need(x_, n, nodes)
    f_x = lagrange_polynom(n, x_, nodes_, all_nodes_table_dict)
    calculated_polynom_values[x_] = f_x
    return f_x


def equation(x_):
    return polynom(x_) - F


def roots_divide(A, B, N):
    segms_counter = 0
    segm_start = A
    h = (B - A) / N
    segm_end = segm_start + h
    f_segm_start = equation(segm_start)

    while segm_end <= B:
        f_segm_end = equation(segm_end)

        if f_segm_start * f_segm_end <= 0:
            segms_counter += 1
            print(f'Сегмент с корнем: [{segm_start}, {segm_end}]')
            if f_segm_start == 0 or f_segm_end == 0:
                if f_segm_start == 0:
                    print('Найден корень: ', segm_start)
                if f_segm_end == 0:
                    print('Найден корень: ', segm_end)
                continue
            segments.append((segm_start, segm_end))
        segm_start = segm_end
        segm_end += h
        f_segm_start = f_segm_end

    print('Всего сегментов, содержащих корень: ', segms_counter)
    print()


def secant(x_prev, x_cur):
    f_x_cur = equation(x_cur)
    f_x_prev = equation(x_prev)

    x_next = x_cur - f_x_cur * (x_cur - x_prev) / (f_x_cur - f_x_prev)

    if abs(x_next - x_cur) < e:
        return x_next, abs(x_next - x_cur)
    return secant(x_cur, x_next)


def print_table(rows_list, is_revers):
    if is_revers:
        dict_we_need = reversed_nodes_table_dict
        table = PrettyTable(['i', 'f(X_i)', 'X_i'])
    else:
        dict_we_need = all_nodes_table_dict
        table = PrettyTable(['i', 'X_i', 'f(X_i)'])

    i = 1
    for key in rows_list:
        table.add_row([i, key, dict_we_need[key]])
        i += 1
    print(table)


print('Задача обратного интерполирования')
print('Вариант 1')
print('Функция: sin(x) - x**2/2')

a, b = map(float, input('Введите через пробел начало и конец отрезка:').split())
m = int(input('Введите m, где m+1 - число значений в таблице:'))
h = (b - a) / m

nodes = [a + i * h for i in range(m + 1)]
all_nodes_table_dict = {x: f(x) for x in nodes}
print("Исходная таблица узел-значение")
print_table(nodes, False)

while True:
    n = int(input(f'Введите n - максимальную степень интерполяционного многочлена, n<={m}:'))
    while n > m:
        print('Некорректное значение n!')
        n = int(input('Введите n - максимальную степень интерполяционного многочлена, n<=m:'))
    F = float(input('Введите значение, для которого нужно найти, в какой точке функция его принимает:'))

    print('Первый способ')
    reversed_nodes = list(all_nodes_table_dict.values())
    reversed_nodes_table_dict = {x[1]: x[0] for x in all_nodes_table_dict.items()}
    selected_nodes = get_nodes_we_need(F, n, reversed_nodes)
    print("Отсортированная в порядке отдаления от x таблица узел-значение")
    print_table(selected_nodes, True)

    L_F = lagrange_polynom(n, F, selected_nodes, reversed_nodes_table_dict)
    print('Приблизим обратную к f функцию с помощью полинома Лагранжа')
    print(f'Значение F = {F} в точке х = ', L_F)
    print(f'ПРОВЕРКА: модуль невязки |f(x)-F| = {abs(f(L_F) - F)}')
    print()
    print('Второй способ')
    print('Решение уравнения P_n - F = 0 выполняется методом секущих')
    deg = int(input('Введите, с какой точностью нужно найти корень (степень 10): '))
    e = 10 ** deg
    calculated_polynom_values = {}
    segments = []
    roots_divide(a, b, 1000)
    if len(segments) == 0:
        print(f'На отрезке[{a},{b}] функция не принимает значение F = {F}')
        continue
    for s in segments:
        root, steps_difference = secant(s[0], s[1])
        print(f'Значение F = {F} в точке х = ', root)
        print('|x_k - x_{k-1}| =', steps_difference)
        print(f'ПРОВЕРКА: модуль невязки |f(x)-F| = {abs(f(root) - F)}')
    print()

    flag = input('Хотите ввести новые значения? (y/n):')
    if flag == 'n':
        break


