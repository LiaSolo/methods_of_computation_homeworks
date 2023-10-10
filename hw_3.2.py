from math import exp
from prettytable import PrettyTable


def f(x_):
    return exp(1.5*x_)


def df(x_):
    return 1.5*exp(1.5*x_)


def ddf(x_):
    return 2.25*exp(1.5*x_)


def print_table(rows_list):
    table = PrettyTable(['i', 'X_i', 'f(X_i)'])

    i = 1
    for key in rows_list:
        table.add_row([i, key, all_nodes_table_dict[key]])
        i += 1
    print(table)


def print_result_table():
    table = PrettyTable(['i', 'X_i', 'f(X_i)',
                         "f'(X_i)чд", "|f'(X_i)чд - f'(X_i)т|",
                         "f''(X_i)чд", "|f''(X_i)чд - f''(X_i)т|"])

    i = 1
    for key in nodes:
        try:
            table.add_row([i, key, all_nodes_table_dict[key],
                           df_dict[key], abs(df(key) - df_dict[key]),
                           ddf_dict[key], abs(ddf(key) - ddf_dict[key])])
        except:
            table.add_row([i, key, all_nodes_table_dict[key],
                           df_dict[key], abs(df(key) - df_dict[key]), '-', '-'])
        i += 1
    print(table)


def df_for_center(i):
    x_plus = nodes[i + 1]
    x_minus = nodes[i - 1]
    # print('center', x_minus, x_plus)
    return (all_nodes_table_dict[x_plus] - all_nodes_table_dict[x_minus]) / (2 * h)


def df_for_first():
    x = nodes[0]
    x_h = nodes[1]
    x_2h = nodes[2]
    f_a = all_nodes_table_dict[x]
    f_a_h = all_nodes_table_dict[x_h]
    f_a_2h = all_nodes_table_dict[x_2h]
    return (-3 * f_a + 4 * f_a_h - f_a_2h) / (2 * h)


def df_for_last():
    x = nodes[-1]
    x_h = nodes[-2]
    x_2h = nodes[-3]
    f_a = all_nodes_table_dict[x]
    f_a_h = all_nodes_table_dict[x_h]
    f_a_2h = all_nodes_table_dict[x_2h]
    return (3 * f_a - 4 * f_a_h + f_a_2h) / (2 * h)


def ddf_for_center(i):
    x = nodes[i]
    x_plus = nodes[i + 1]
    x_minus = nodes[i - 1]
    f_x = all_nodes_table_dict[x]
    f_x_minus = all_nodes_table_dict[x_minus]
    f_x_plus = all_nodes_table_dict[x_plus]
    print(i, x_plus, x, x_minus)
    return (f_x_plus - 2*f_x + f_x_minus) / h**2


while True:

    a = float(input('Введите начало отрезка: '))
    h = float(input('Укажите, с каким шагом узлы будут отстоять друг от друга: '))
    m = int(input('Введите m, где m+1 - число значений в таблице'))

    # a = 1
    # h = 10**(-11)
    # Почему погрешность сначала уменьшается, а потом увеличивается?
    # На 10**(-12) огромная погрешность
    # На 10**(-11) все нули
    # m = 10

    nodes = [a + i * h for i in range(m + 1)]
    b = nodes[-1]
    all_nodes_table_dict = {x: f(x) for x in nodes}
    df_dict = {}
    ddf_dict = {}
    print("Исходная таблица узел-значение")
    print_table(nodes)

    df_dict[nodes[0]] = df_for_first()
    for i in range(1, m):
        x = nodes[i]
        df_dict[x] = df_for_center(i)
    df_dict[nodes[-1]] = df_for_last()

    ddf_dict[nodes[0]] = '-'
    for i in range(1, m):
        x = nodes[i]
        ddf_dict[x] = ddf_for_center(i)
    ddf_dict[nodes[-1]] = '-'

    print_result_table()

    flag = input('Хотите ввести новые значения? (y/n):')
    if flag == 'n':
        break
