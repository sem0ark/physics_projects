import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt
from matplotlib import rc

# self.points -> (p_n, v_n, type)


class Compute:
    def __init__(self, points, freedom_coef):
        self.points = points
        self.I = freedom_coef
        self.STEPS = 16385

    def remember_calculations(self):
        self.work = self.calculate_work()
        self.energy = self.calculate_inner_energy()
        self.heat = self.calculate_heat(self.work, self.energy)

        self.coef = self.calculate_coef(self.heat, self.work)
        
        self.all_work = sum(self.work)
        self.all_heat = sum(self.heat)
        self.all_energy = sum(self.energy)
        self.heater_heat = sum(i for i in self.heat if i > 0)
        self.cooler_heat = sum(i for i in self.heat if i < 0)


    def l_func(self, p1,v1,p2,v2):
        x = np.linspace(v1, v2, self.STEPS)
        y = np.linspace(p1, p2, self.STEPS)

        return x, y

    def c_func(self, p1,v1,p2,v2):
        x = np.linspace(v1, v2, self.STEPS)
        a = v1*v2*(p1-p2)/(v2-v1)
        b = (p2*v2-p1*v1)/(v2-v1)
        y = a/x + b

        return x, y

    def a_func(self, p1,v1,p2,v2):
        g = 1 + 2/self.I
        x = np.linspace(v1, v2, self.STEPS)
        t1 = v1**g
        t2 = v2**g
        a = t1*t2*(p1-p2)/(t2-t1)
        b = (p2*t2-p1*t1)/(t2-t1)
        y = a/(x**g) + b

        return x, y

    def get_work_l(self, p1,v1,p2,v2):
        x, y = self.l_func(p1,v1,p2,v2)
        work = simps(y,x)
        return work

    def get_work_c(self, p1,v1,p2,v2):
        x, y = self.c_func(p1,v1,p2,v2)
        work = simps(y,x)
        return work

    def get_work_a(self, p1,v1,p2,v2):
        x, y = self.a_func(p1,v1,p2,v2)
        work = simps(y,x)
        return work

    def calculate_work(self):
        work = []
        for i in range(len(self.points)):
            p1, v1, t = self.points[i]
            p2, v2, _ = self.points[(i+1)%len(self.points)]
            
            if v1==v2:
                work.append(0)
            elif t=='l':
                work.append(self.get_work_l(p1,v1,p2,v2))
            elif t=='c':
                work.append(self.get_work_c(p1,v1,p2,v2))
            elif t=='a':
                work.append(self.get_work_a(p1,v1,p2,v2))

        return work

    def calculate_inner_energy(self):
        energy = []
        for i in range(len(self.points)):
            p1, v1, t = self.points[i]
            p2, v2, _ = self.points[(i+1)%len(self.points)]

            energ1 = self.I * (p2*v2 - p1*v1) / 2

            energy.append(energ1)

        return energy

    def calculate_heat(self, work, energy):
        return [i+j for i,j in zip(work, energy)]

    def calculate_coef(self, heat, work):
        all_work = sum(work)
        heater_heat = sum(i for i in heat if i > 0)

        return all_work/heater_heat



class Draw:
    def __init__(self, points, i_coef):
        self.comp = Compute(points, i_coef)
        self.points = points

    def create_graph(self):
        y = np.array([])
        x = np.array([])

        for i in range(len(self.points)):
            p1, v1, t = self.points[i]
            p2, v2, _ = self.points[(i+1)%len(self.points)]

            if t=='l':
                dx, dy = self.comp.l_func(p1,v1,p2,v2)
                y = np.append(y, dy)
                x = np.append(x, dx)
            elif t=='c':
                dx, dy = self.comp.c_func(p1,v1,p2,v2)
                y = np.append(y, dy)
                x = np.append(x, dx)
            elif t=='a':
                dx, dy = self.comp.a_func(p1,v1,p2,v2)
                y = np.append(y, dy)
                x = np.append(x, dx)

        return x, y

    def plot_graph(self, x_graph, y_graph):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set(
            ylabel='p (Па)',
            xlabel='V (м^3)'
        )
        ax.ticklabel_format(
            style='sci', axis='y',
            scilimits=(-2, 3),
            useMathText=True
        )
        ax.ticklabel_format(
            style='sci', axis='x',
            scilimits=(-2, 3),
            useMathText=True
        )
        
        ax.plot(x_graph, y_graph)

        plt.tight_layout()
        plt.show()

    def show(self):
        self.plot_graph(*self.create_graph())

if __name__ == '__main__':
    test = [
        (2, 2, 'c'),
        (1, 4, 'a'),
        (1, 3.28134142, 'c'),
        (2, 1.64067071, 'a')
    ]

    d = Draw(test, 5)
    d.comp.remember_calculations()
    print(d.comp.work)
    print(d.comp.heat)
    print(d.comp.energy)
    print(d.comp.coef)
    d.show()
