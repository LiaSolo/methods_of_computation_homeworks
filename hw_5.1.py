from scipy.integrate import quad
from math import sin, sqrt
from numpy.linalg import solve


def f(x):
    return sin(x)


def weight(x):
    return sqrt(x / (1 - x))


def polynom_deg_m(x, m):
    poly = 0
    for i in range(m+1):
        poly += x**i
    return poly


def get_ikf(func, ro, a, b, n, nodes):
    moments = list()
    res = 0
    for i in range(n):
        moments.append(quad(lambda x: x ** i * ro(x), a, b)[0])

    mtrx = [list(map(lambda x: x ** j, nodes)) for j in range(n)]
    coeffs = solve(mtrx, moments)
    for i in range(n):
        res += coeffs[i]*func(nodes[i])
    return moments, coeffs, res


def ikf_checking_on_poly(a, b, n, nodes):
    exact = quad(lambda x: polynom_deg_m(x, n-1), a, b)[0]
    res = get_ikf(lambda x: polynom_deg_m(x, n-1), lambda x: 1, a, b, n, nodes)[2]
    print()
    print(f'=== Проверка на полиноме степени {n-1} ===')
    print(f'"Точное" значение интеграла: {exact}')
    print(f'Значение интеграла, вычисленное с помощью ИКФ: {res}')
    print(f'Погрешность: {abs(res - exact)}')
    print()


def w(x, a: list, n):
    a.append(1)
    poly = 0
    for i in range(n+1):
        poly += x**i * a[i]
    return poly


def roots_divide(func, A, B, N):
    segments = list()
    segm_start = A
    h = (B - A) / N
    segm_end = segm_start + h
    f_segm_start = func(segm_start)

    while segm_end <= B:
        f_segm_end = func(segm_end)

        if f_segm_start * f_segm_end <= 0:
            segments.append((segm_start, segm_end))
        segm_start = segm_end
        segm_end += h
        f_segm_start = f_segm_end
    return segments


def bisection(func, segm: tuple):
    e = 10**(-13)
    begin = segm[0]
    end = segm[1]
    mid = (begin + end) / 2
    if (end - begin) < 2 * e:
        return mid, end - begin
    elif func(begin) * func(mid) < 0:
        return bisection(func, (begin, mid))
    else:
        return bisection(func, (mid, end))


def get_kf_nast(func, ro, a, b, n):
    moments = list()
    roots = list()
    for i in range(2*n):
        moments.append(quad(lambda x: x ** i * ro(x), a, b)[0])

    mtrx = [[moments[i + j] for j in range(n)] for i in range(n)]
    coeffs = list(solve(mtrx, [-1*mu for mu in moments[n:]]))

    segments = roots_divide(lambda x: w(x, coeffs, n), a, b, 1000)
    for s in segments:
        roots.append(bisection(lambda x: w(x, coeffs, n), s)[0])

    res = get_ikf(func, ro, a, b, n, roots)[2]
    return moments, coeffs, res, roots


def kf_nast_checking_on_poly(a, b, n):
    exact = quad(lambda x: x**(2*n-1), a, b)[0]
    res = get_kf_nast(lambda x: x**(2*n-1), lambda x: 1, a, b, n)[2]
    print()
    print(f'=== Проверка на одночлене степени {2*n-1} ===')
    print(f'"Точное" значение интеграла: {exact}')
    print(f'Значение интеграла, вычисленное с помощью КФ НАСТ: {res}')
    print(f'Погрешность: {abs(res - exact)}')
    print()


print('Приближенное вычисление интегралов при помощи квадратурных формул '
      'Наивысшей Алгебраической Степени Точности')


def main():
    print('Вес: sqrt(x / (1-x))')
    print('Функция: sin(x)')
    a = b = 10
    while a < 0 or b > 1:
        a, b = map(float, input('Введите начало и конец отрезка через пробел: ').split())
    nodes = []
    n = 0
    while n < 2:
        n = int(input('Укажите, по какому количеству узлов строить ИКФ (минимум 2): '))

    for i in range(n):
        node = float(input(f'Введите узел {i + 1}: '))
        while node in nodes:
            print('Такой узел уже указан. Необходимы попарно различные')
            node = float(input(f'Введите узел {i + 1}: '))
        nodes.append(node)

    print()
    print('=== Вычисление ИКФ ===')

    moments, coeffs, res = get_ikf(f, weight, a, b, n, nodes)
    for i in range(n):
        print(f'Момент {i}: {moments[i]}')
    for i in range(n):
        print(f'Коэффициент {i} ИКФ: {coeffs[i]}')

    exact = quad(lambda x: f(x) * weight(x), a, b)[0]
    print(f'"Точное" значение интеграла: {exact}')
    print(f'Значение интеграла, вычисленное с помощью ИКФ: {res}')
    print(f'Погрешность: {abs(res - exact)}')

    ikf_checking_on_poly(a, b, n, nodes)

    print('=== Вычисление КФ НАСТ ===')

    moments, coeffs, res, roots = get_kf_nast(f, weight, a, b, n)
    print('Узлы, по которым строим КФ НАСТ')
    print(roots)
    for i in range(2*n):
        print(f'Момент {i}: {moments[i]}')
    for i in range(n):
        print(f'Коэффициент {i} КФ НАСТ: {coeffs[i]}')

    exact = quad(lambda x: f(x) * weight(x), a, b)[0]
    print(f'"Точное" значение интеграла: {exact}')
    print(f'Значение интеграла, вычисленное с помощью КФ НАСТ: {res}')
    print(f'Погрешность: {abs(res - exact)}')

    kf_nast_checking_on_poly(a, b, n)


while True:
    main()
    _ = input('Повторить?')
