from math import exp

# A = -1
# B = 3
# e = 10**(-8)
# -2.513, 0, 1.4776 < x < 1.4777
segments = list()


def f(x): return (x-1) * (x-1) - exp(-x)
def df(x): return 2 * (x - 1) + exp(-x)
def ddf(x): return 2 - exp(-x)


def is_x0_ok(x):
    if f(x) * ddf(x) < 0:
        return False
    return True


# пробую середину, если не подходит, то
# начинаю искать с начала с швгом h
def choose_x0_for_newton(segm):
    begin = segm[0]
    end = segm[1]
    h = (begin - end) / 10000
    x_0 = (begin + end) / 2
    if f(x_0) * ddf(x_0) > 0:
        return x_0
    # если не подошла середина отрезка, то начинаем идти с начала с небольшим шагом
    x_0 = begin
    while f(x_0) * ddf(x_0) < 0:
        print('Неподходящий x_0, т.к. f(x_0) * ddf(x_0) < 0:')
        print(f'f(x_0) = {f(x_0)}, ddf(x_0) = {ddf(x_0)}')
        x_0 += h
        if x_0 > end:
            raise Exception(f'Сходимости на сегменте [{begin}, {end}] не будет')
    return x_0


def bisection(steps, segm: tuple):
    steps += 1
    begin = segm[0]
    end = segm[1]
    mid = (begin + end) / 2
    if (end - begin) < 2 * e:
        return mid, steps, end - begin
    elif f(begin) * f(mid) < 0:
        return bisection(steps, (begin, mid))
    else:
        return bisection(steps, (mid, end))


def newton(steps, x_curr):
    steps += 1
    x_next = x_curr - f(x_curr) / df(x_curr)

    if abs(x_curr - x_next) < e:
        return x_next, steps, abs(x_curr - x_next)
    return newton(steps, x_next)


def m_newton(steps, x_curr):
    steps += 1
    x_next = x_curr - f(x_curr) / d

    if abs(x_next - x_curr) < e:
        return x_next, steps, abs(x_next - x_curr)
    return m_newton(steps, x_next)


def secant(steps, x_prev, x_cur):
    steps += 1
    x_next = x_cur - f(x_cur) * (x_cur - x_prev) / (f(x_cur) - f(x_prev))

    if abs(x_next - x_cur) < e:
        return x_next, steps, abs(x_next - x_cur)
    return secant(steps, x_cur, x_next)


def roots_divide(A, B, N):
    segms_counter = 0
    segm_start = A
    h = (B - A) / N
    segm_end = segm_start + h
    f_segm_start = f(segm_start)

    while segm_end <= B:
        f_segm_end = f(segm_end)

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

    print('Всего сегментоа, содержащих корень: ', segms_counter)
    print()


while True:
    print('Численные методы решения нелинейных уравнений')
    print('Начальные данные:')
    try:
        A, B = map(int, input('Введите концы отрезка [A, B] через пробел: ').split())
        if A >= B:
            print('Необходимо, чтобы начало отрезка было меньше, чем конец')
        deg = int(input('Введите, с какой точностью нужно найти корень (степень 10): '))
        e = 10**deg
        N = int(input('Введите параметр N: '))
        roots_divide(A, B, N)
    except:
        print('Будьте осторожнее с вводом параметров')
        continue

    print('a. Метод половинного деления (метод бисекции)')
    for s in segments:
        root, steps, steps_difference = bisection(0, s)
        print('Сегмент:', f'[{s[0]}, {s[1]}]')
        print('Начальное приближение к корню:', (s[0] + s[1]) / 2)
        print('Количество шагов для достижения точности е:', steps)
        print('Корень:', root)
        print('Длина последнего отрезка:', steps_difference)
        print('Абсолютная величина невязки:', abs(f(root)))
        print()

    print('b. Метод Ньютона (метод касательных)')
    for s in segments:
        x_0 = choose_x0_for_newton(s)
        root, steps, steps_difference = newton(0, x_0)
        print('Сегмент:', f'[{s[0]}, {s[1]}]')
        print('Начальное приближение к корню:', x_0)
        print('Количество шагов для достижения точности е:', steps)
        print('Корень:', root)
        print('|x_k - x_{k-1}| =', steps_difference)
        print('Абсолютная величина невязки:', abs(f(root)))
        print()

    print('c. Модифицированный метод Ньютона')
    for s in segments:
        x_0 = choose_x0_for_newton(s)
        d = df(x_0)
        x_1 = x_0 - f(x_0) / d
        root, steps, steps_difference = m_newton(0, (s[1] + s[0]) / 2)
        print('Сегмент:', f'[{s[0]}, {s[1]}]')
        print('Начальное приближение к корню:', x_0)
        print('Количество шагов для достижения точности е:', steps)
        print('Корень:', root)
        print('|x_k - x_{k-1}| =', steps_difference)
        print('Абсолютная величина невязки:', abs(f(root)))
        print()

    print('d. Метод секущих')
    for s in segments:
        x_0 = s[0]
        x_1 = s[1]
        root, steps, steps_difference = secant(0, x_0, x_1)
        print('Сегмент:', f'[{s[0]}, {s[1]}]')
        print(f'Начальные приближения к корню: {x_0}, {x_1}')
        print('Количество шагов для достижения точности е:', steps)
        print('Корень:', root)
        print('|x_k - x_{k-1}| =', steps_difference)
        print('Абсолютная величина невязки:', abs(f(root)))
        print()

    segments.clear()




