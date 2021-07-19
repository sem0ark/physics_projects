import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np


def main():
    mode = int(input('Выберите режим 1)pV  2)pT  3)VT : '))
    n = int(input('Введите кол-во точек: '))
    fg = input('График цикличный (да/нет): ').strip().lower() == 'да'
    if mode == 1:
        run_pV(n, closed=fg)
    elif mode == 2:
        run_pT(n, closed=fg)
    elif mode == 3:
        run_VT(n, closed=fg)


def input_lines(x, y, closed):
    lines = []
    print('Введите тип линий: l - прямая, c - гипербола: ')
    for i in range(len(x) - 1):
        type_ = input(f'{i + 1}-{i + 2}: ')
        lines.append((x[i], y[i], x[i + 1], y[i + 1], type_))
    if closed:
        type_ = input(f'{len(x)}-{1}: ')
        lines.append((x[-1], y[-1], x[0], y[0], type_))

    return lines


def run_pV(n, closed=True):
    print('Для каждой точки введите текущее давление(Па) объём(м^3)')
    print('Пример: 20000 0.3')
    dots_p = []
    dots_V = []
    for i in range(n):
        p, V = map(float, input(f'Точка №{i+1}: ').split())
        dots_p.append(p)
        dots_V.append(V)

    lines = input_lines(dots_V, dots_p, closed)
    plot_pV(lines, list(zip(dots_V, dots_p)))


def run_pT(n, closed=True):
    print('Для каждой точки введите текущее давление(Па) температуру(K)')
    print('Пример: 20000 300')
    dots_p = []
    dots_T = []
    for i in range(n):
        p, T = map(float, input(f'Точка №{i+1}: ').split())
        dots_p.append(p)
        dots_T.append(T)
    lines = input_lines(dots_T, dots_p, closed)
    plot_pT(lines, list(zip(dots_T, dots_p)))


def run_VT(n, closed=True):
    print('Для каждой точки введите текущий объём(м^3) температуру(K)')
    print('Пример: 20 300')
    dots_V = []
    dots_T = []
    for i in range(n):
        V, T = map(float, input(f'Точка №{i+1}: ').split())
        dots_V.append(V)
        dots_T.append(T)

    lines = input_lines(dots_T, dots_V, closed)
    plot_VT(lines, list(zip(dots_T, dots_V)))


def find_p(T, V, c):
    return c*T/V


def find_V(T, p, c):
    return c*T/p


def find_T(p, V, c):
    return p*V/c


def generate_line_l(x1, y1, x2, y2, steps):
    x = np.linspace(x1, x2, steps)
    y = np.linspace(y1, y2, steps)
    return x, y


def generate_line_c(x1, y1, x2, y2, steps):
    x = np.linspace(x1, x2, steps)
    a = x1*x2*(y1-y2)/(x2-x1)
    b = (y2*x2-y1*x1)/(x2-x1)
    y = a/x + b
    return x, y


def plot_pV(lines, dots_Vp):
    print('const = m*R/M')
    c = float(input('Введите const: '))

    p = np.array([])
    V = np.array([])
    T = np.array([])

    dots = []
    for Vj, pj in dots_Vp:
        Tj = find_T(pj, Vj, c)
        dots.append((Vj, Tj, pj))

    for i in lines:
        V1, p1, V2, p2, type_ = i

        if type_ == 'l':
            lV, lp = generate_line_l(V1, p1, V2, p2, 100)
            lT = find_T(lp, lV, c)
        else:
            lV, lp = generate_line_c(V1, p1, V2, p2, 100)
            lT = find_T(lp, lV, c)
        p = np.append(p, lp)
        V = np.append(V, lV)
        T = np.append(T, lT)
    draw(p, V, T, dots)


def plot_pT(lines, dots_Tp):
    print('const = m*R/M')
    c = float(input('Введите const: '))

    p = np.array([])
    V = np.array([])
    T = np.array([])

    dots = []
    for Tj, pj in dots_Tp:
        Vj = find_V(Tj, pj, c)
        dots.append((Vj, Tj, pj))

    for i in lines:
        T1, p1, T2, p2, type_ = i
        if type_ == 'l':
            lT, lp = generate_line_l(T1, p1, T2, p2, 100)
            lV = find_V(lT, lp, c)
        else:
            lT, lp = generate_line_c(T1, p1, T2, p2, 100)
            lV = find_V(lT, lp, c)
        p = np.append(p, lp)
        V = np.append(V, lV)
        T = np.append(T, lT)
    draw(p, V, T, dots)


def plot_VT(lines, dots_TV):
    print('const = m*R/M')
    c = float(input('Введите const: '))

    p = np.array([])
    V = np.array([])
    T = np.array([])

    dots = []
    for Tj, Vj in dots_TV:
        pj = find_p(Tj, Vj, c)
        dots.append((Vj, Tj, pj))

    for i in lines:
        T1, V1, T2, V2, type_ = i

        if type_ == 'l':
            lT, lV = generate_line_l(T1, V1, T2, V2, 100)
            lp = find_p(lT, lV, c)
        else:
            lT, lV = generate_line_l(T1, V1, T2, V2, 100)
            lp = find_p(lT, lV, c)
        p = np.append(p, lp)
        V = np.append(V, lV)
        T = np.append(T, lT)
    draw(p, V, T, dots)


def draw(p, V, T, dots):
    rc('xtick', labelsize=8)
    rc('ytick', labelsize=8)

    T_dot = [i[1] for i in dots]
    V_dot = [i[0] for i in dots]
    p_dot = [i[2] for i in dots]

    fig1 = plt.figure()

    ax1 = fig1.gca(projection='3d', proj_type='ortho')
    ax1.plot(V, T, p)
    ax1.plot(V_dot, T_dot, p_dot, 'r.')
    for i, (x, y, z) in enumerate(zip(V_dot, T_dot, p_dot)):
        ax1.text(x, y, z, s=str(i+1), fontstyle='oblique', fontsize='large', color="g")
    ax1.set_xlabel('Объём (м^3)')
    ax1.set_ylabel('Температура (K)')
    ax1.set_zlabel('Давление (Па)')
    ax1.ticklabel_format(style='sci', axis='both', scilimits=(-2, 3), useMathText=True)

    fig2, [a1, a2, a3] = plt.subplots(1, 3, figsize=(12, 4))

    a1.plot(T, p)
    a1.plot(T_dot, p_dot, 'r.')
    for i, (x, y) in enumerate(zip(T_dot, p_dot)):
        a1.text(x, y, s=str(i+1), fontstyle='oblique', fontsize='large', color="g")
    a1.ticklabel_format(style='sci', axis='both', scilimits=(-2, 3), useMathText=True)
    a1.set_xlabel('Температура (K)')
    a1.set_ylabel('Давление (Па)')

    a2.plot(T, V)
    a2.plot(T_dot, V_dot, 'r.')
    for i, (x, y) in enumerate(zip(T_dot, V_dot)):
        a2.text(x, y, s=str(i+1), fontstyle='oblique', fontsize='large', color="g")
    a2.ticklabel_format(style='sci', axis='both', scilimits=(-2, 3), useMathText=True)
    a2.set_xlabel('Температура (K)')
    a2.set_ylabel('Объём (м^3)')

    a3.plot(V, p)
    a3.plot(V_dot, p_dot, 'r.')
    for i, (x, y) in enumerate(zip(V_dot, p_dot)):
        a3.text(x, y, s=str(i+1), fontstyle='oblique', fontsize='large', color="g")
    a3.ticklabel_format(style='sci', axis='both', scilimits=(-2, 3), useMathText=True)
    a3.set_xlabel('Объём (м^3)')
    a3.set_ylabel('Давление (Пa)')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
