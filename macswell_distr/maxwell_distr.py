import matplotlib.pyplot as plt
from numpy import exp, pi


def maxwell_distr(v, T, M):
    R = 8.314462618

    def f(x):
        return 4*pi*((M/(2*pi*R*T))**1.5)*(x**2)*exp(-(M*(x**2))/(2*R*T))

    return list(map(f, v))


def run():
    n = int(input('Введите число графиков: '))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set(xlabel='Скорость (м/с)',
           title='Распределение Максвелла')
    ax.grid()
    # ax.set_box_aspect(1)
    print('Введите для каждого графика температуру (К) и молярную массу (кг/моль)')
    print('Например: 300 0.028')
    for _ in range(n):
        T ,M = map(float, input().split())
        x = range(20000)
        y = maxwell_distr(x, T, M)
        ax.plot(list(x), y, label=f'T={T}K M={M}кг/моль')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(-2, 3), useMathText=True)
        ax.set_xlim(0,2000)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    run()
