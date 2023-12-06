from math import sin
from scipy.integrate import quad
from prettytable import PrettyTable


def f(x):
    return sin(x) / x


def get_legendre_poly(index):
    if index == 0:
        return lambda x: 1
    if index == 1:
        return lambda x: x
    coef_1 = (2 * index - 1) / index
    coef_2 = (index - 1) / index
    poly_1 = get_legendre_poly(index - 1)
    poly_2 = get_legendre_poly(index - 2)
    return lambda x: coef_1*poly_1(x)*x - coef_2*poly_2(x)


def roots_divide(func):
    segments = list()
    segm_start = -1
    h = 2 / 1000
    segm_end = segm_start + h
    f_segm_start = func(segm_start)

    while segm_end <= 1:
        f_segm_end = func(segm_end)

        if f_segm_start * f_segm_end <= 0:
            segments.append((segm_start, segm_end))
        segm_start = segm_end
        segm_end += h
        f_segm_start = f_segm_end
    return segments


def secant(func, x_prev, x_cur):
    e = 10**(-12)
    x_next = x_cur - func(x_cur) * (x_cur - x_prev) / (func(x_cur) - func(x_prev))

    if abs(x_next - x_cur) < e:
        return x_next, abs(x_next - x_cur)
    return secant(func, x_cur, x_next)


def get_coefficients(poly, nodes, num_nodes):
    return [2*(1-nodes[i]**2)/(num_nodes*poly(nodes[i]))**2 for i in range(num_nodes)]


def get_kf_gauss(func, a, b, num_nodes):
    roots = list()
    poly = [get_legendre_poly(i) for i in range(num_nodes + 1)]
    segments = roots_divide(poly[-1])
    for s in segments:
        root = secant(poly[-1], s[0], s[1])[0]
        roots.append(root)

    coefficients = get_coefficients(poly[-2], roots, num_nodes)
    ans = 0
    for i in range(num_nodes):
        x = (b - a) / 2 * roots[i] + (b + a) / 2
        ans += coefficients[i] * func(x)
    ans *= (b - a) / 2

    return ans, roots, coefficients


def print_table(nodes, coeffs):
    table = PrettyTable(['i', 'x_i', 'A_i'])

    i = 1
    for i in range(len(nodes)):
        table.add_row([i+1, nodes[i], coeffs[i]])
    print(table)


def check_on_poly(a, b, num_nodes):
    print(f'Количество узлов: {num_nodes}')
    print(f'Степень полинома: {2*num_nodes-1}')
    def poly(x): return x**(2*num_nodes-1)
    def integral(x): return x**(2*num_nodes)/(2*num_nodes)
    exact = integral(b) - integral(a)
    answer = get_kf_gauss(poly, a, b, num_nodes)[0]
    print(f'"Точное" значение интеграла: {exact}')
    print(f'Значение интеграла, полученное с помощью КФ Гаусса: {answer}')
    print(f'Погрешность: {abs(exact - answer)}')


def main():
    a, b = map(float, input('Введите концы отрезка интегрирования через пробел: ').split())
    num_nodes = list(map(int, input('Введите три желаемых количества узлов через пробел: ').split()))
    exact = quad(f, a, b)[0]
    print('======================================')
    print(f'"Точное" значение интеграла: {exact}')
    for i in range(3):
        print()
        answer, roots, coeffs = get_kf_gauss(f, a, b, num_nodes[i])
        print(f'Количество узлов: N_{i+1} = {num_nodes[i]}')
        print("Таблица узел <-> коэффициент")
        print_table(roots, coeffs)
        print(f'Значение интеграла, полученное с помощью КФ Гаусса: {answer}')
        print(f'Погрешность: {abs(exact - answer)}')

    print('\n===Проверка на полиномах===')
    for i in range(3):
        print()
        check_on_poly(a, b, num_nodes[i])


while True:
    main()
    _ = input('Повторить? ')
