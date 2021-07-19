from math import hypot
import matplotlib.pyplot as plt
import numpy as np

class Charge:
    K = 9*10**9
    
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q

    def getDist(self, X, Y):
        return

    def getEVector(self, X, Y):
        return

class PointCharge(Charge):
    def __init__(self, x, y, q):
        super().__init__(x, y, q)
    
    def getDist(self, X, Y):
        rx = X-self.x
        ry = Y-self.y
        rl = np.maximum(np.sqrt(rx**2 + ry**2), 0.0001)

        return rl, rx, ry

    def getEVector(self, X, Y):
        r, rx, ry = self.getDist(X, Y)
        E  = self.q / r**2
        Ex = E * np.divide(rx , r) * self.K
        Ey = E * np.divide(ry , r) * self.K

        return Ex, Ey

def getEField(wx, wy, px, py, charges):
    x = np.arange(-wx, wx, px)
    y = np.arange(-wy, wy, py)
    X, Y = np.meshgrid(x, y)
    U, V = np.zeros(X.shape), np.zeros(Y.shape)
    for charge in charges:
        tU, tV = charge.getEVector(X, Y)
        U += tU
        V += tV
    return X, Y, U, V

def main():
    n = int(input('Введите кол-во зарядов: '))
    charges = []
    b = [[], []]
    r = [[], []]

    print('Введите координаты (от -5 до 5) заряж. тела и его заряд(Кл)')
    
    for _ in range(n):
        x, y, q = map(float, input().split(' '))
        charges.append(PointCharge(x, y, q))
        if q >= 0:
            r[0].append(x)
            r[1].append(y)
        else:
            b[0].append(x)
            b[1].append(y)
    print('Подождите, идёт расчёт...')

    b = np.array(b)
    r = np.array(r)

    X, Y, U, V = getEField(5, 5, 0.0501, 0.0501, charges)

    fig, ax = plt.subplots(figsize=(8,8))
    ax.streamplot(X, Y, U, V, linewidth=0.5, arrowsize=0.8, density=3.5, color='k', zorder=1, minlength=0.02)

    ax.set_title('Линии электростатического поля')
    
    ax.scatter(b[0], b[1], 200, linewidth=3, color='b', zorder=10)
    ax.scatter(r[0], r[1], 200, linewidth=3, color='r', zorder=10)

    X, Y, U, V = getEField(5, 5, 0.2501, 0.2501, charges)

    fig2, ax2 = plt.subplots(figsize=(7,7))

    R = np.sqrt(U**2 + V**2)
    ax2.quiver(X, Y, np.divide(U, R), np.divide(V, R), scale=60, linewidth=0.5, linestyle='-', zorder=1, width=0.002)
    ax2.set_title('Линии электростатического поля')
    
    ax2.scatter(b[0], b[1], 200, linewidth=3, color='b', zorder=10)
    ax2.scatter(r[0], r[1], 200, linewidth=3, color='r', zorder=10)
    
    fig.tight_layout()
    fig2.tight_layout()

    print('Готово!')
    
    plt.show()

if __name__ == '__main__':
    while True:
        print('-'*20)
        try:
            main()
        except Exception as e:
            print('something went wrong')
            print(e)
