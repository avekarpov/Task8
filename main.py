import numpy
import matplotlib.pyplot as plt
import copy


dx = 0.05
dy = 0.025
dt = 0.0001

if dt / (dx ** 2) + dt / (dy ** 2) >= 0.5:
    raise RuntimeError('dt must more small')


def difference_scheme(values, i, j):
    if i == 0 or i == len(values) - 1 or j == 0 or j == len(values[0]) - 1:
        raise  # error

    return (values[j + 1, i] + values[j - 1, i] + values[j, i - 1] + values[j, i + 1]) / 4.


def modulation(x_len, y_len, time=-1, precision=1e-6):
    ax = plt.axes(projection='3d')

    def x_left_boundary_dx(y, next):  # du/dx(0, y) = 0  # left
        return next

    def x_right_boundary(y):  # u(2, y) = -sin(3 * pi * y)  # right
        return numpy.sin(3 * numpy.pi * y)

    def y_left_boundary(x):  # u(x, 0) = 0  # top
        return 0

    def y_right_boundary(x):  # u(x, 1) = -cos(7 * pi * x / 4)  # bottom
        return -numpy.cos(7 * numpy.pi * x / 4)

    def initial_condition(x, y):  # u(x, y) = 0, t = 0
        return 1

    t = 0

    xs = numpy.arange(0, x_len + 0.5 * dx, dx)
    ys = numpy.arange(0, y_len + 0.5 * dy, dy)
    us_next = numpy.empty((ys.size, xs.size))

    def boundaries():
        for i in range(ys.size - 1):  # left
            us_next[i, 0] = x_left_boundary_dx(ys[i], us_next[i + 1, 0])

        for i in range(ys.size):  # right
            us_next[i, -1] = x_right_boundary(ys[i])

        for i in range(xs.size):  # top
            us_next[0, i] = y_left_boundary(xs[i])

        for i in range(xs.size):  # bottom
            us_next[-1, i] = y_right_boundary(xs[i])

    for i in range(xs.size):  # whole
        for j in range(ys.size):
            us_next[j, i] = initial_condition(xs[i], xs[j])

    boundaries()

    us = copy.deepcopy(us_next)

    if time == 0:
        xxs, yys = numpy.meshgrid(xs, ys)
        ax.plot_surface(xxs, yys, us, rstride=1, cstride=1, cmap='viridis')

    t += dt

    print('Start calc')

    while time == -1 or time:
        print('t:', t, end=' ')

        for i in range(1, xs.size - 1):
            for j in range(1, ys.size - 1):
                us_next[j, i] = difference_scheme(us, i, j)

        boundaries()

        dif = 0
        for i in range(xs.size):
            for j in range(ys.size):
                dif += abs(us[j, i] - us_next[j, i])
        dif /= xs.size * ys.size
        print("dif:", dif)
        if dif < precision:
            xxs, yys = numpy.meshgrid(xs, ys)
            ax.plot_surface(xxs, yys, us, rstride=1, cstride=1, cmap='viridis')
            break

        us = copy.deepcopy(us_next)

        if time != -1 and t >= time:
            xxs, yys = numpy.meshgrid(xs, ys)
            ax.plot_surface(xxs, yys, us, rstride=1, cstride=1, cmap='viridis')
            break

        t += dt

    print('End calc')
    plt.show()


modulation(2, 1, -1)
