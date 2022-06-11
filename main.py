import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy


dx = 0.05
dy = 0.05
dt = 0.0001

if dt / (dx ** 2) + dt / (dy ** 2) >= 0.5:
    raise RuntimeError('dt must more small')


def difference_scheme(values, i, j):
    if i == 0 or i == len(values) - 1 or j == 0 or j == len(values[0]) - 1:
        raise  # error

    return (values[i][j + 1] + values[i][j - 1] + values[i - 1][j] + values[i + 1][j]) / 4.


def modulation(x0, x_len, y0, y_len):
    slice_ax_n = 10
    slice_ax = 'y'

    def x_left_boundary_dx(y, next):  # du/dx(0, y) = 0
        return next

    def x_right_boundary(y):  # u(2, y) = -sin(3 * pi * y)
        return -math.sin(3 * math.pi * y)

    def y_left_boundary(x):  # u(x, 0) = 0
        return 0

    def y_right_boundary(x):  # u(x, 1) = -cos(7 * pi * x / 4)
        return -math.cos(7 * math.pi * x / 4)

    def initial_condition(x, y):  # u(x, y) = 0, t = 0
        return 1

    frames = []
    fig, ax = plt.subplots()

    x = x0
    y = y0
    t = 0
    xs = []
    ys = []
    ts = []
    us_next = []

    ts.append(t)

    while x < x_len:
        xs.append(x)
        x += dx

    while y < y_len:
        ys.append(y)
        y += dy

    for i in range(0, len(xs)):
        us_next.append([])
        for j in range(0, len(ys)):
            us_next[i].append(initial_condition(xs[i], ys[j]))

    for i in range(len(xs) - 1):
        us_next[i][0] = x_left_boundary_dx(xs[i], us_next[i + 1][0])
        us_next[i][-1] = x_right_boundary(xs[i])

    for i in range(len(ys) - 1):
        us_next[0][i] = y_left_boundary(ys[i])
        us_next[-1][i] = y_right_boundary(ys[i])

    us = copy.deepcopy(us_next)

    t += dt

    if slice_ax == 'x':
        line = []
        for i in range(len(ys)):
            line.append(us[slice_ax_n][i])
        line = ax.plot(ys, line, '-b')
        frames.append(line)
    elif slice_ax == 'y':
        line = []
        for i in range(len(xs)):
            line.append(us[i][slice_ax_n])
        line = ax.plot(xs, line, '-b')
        frames.append(line)

    print('Start calc')

    while True:
        print('t:', t, end=' ')

        ts.append(t)

        for i in range(1, len(xs) - 1):
            for j in range(1, len(ys) - 1):
                us_next[i][j] = difference_scheme(us, i, j)

        for i in range(len(xs) - 1):
            us_next[i][0] = x_left_boundary_dx(xs[i], us_next[i + 1][0])
            us_next[i][-1] = x_right_boundary(xs[i])

        for i in range(len(ys) - 1):
            us_next[0][i] = y_left_boundary(ys[i])
            us_next[-1][i] = y_right_boundary(ys[i])

        dif = 0
        for i in range(len(us)):
            for j in range(len(us[0])):
                dif += us[i][j] - us_next[i][j]
        dif = abs(dif)
        print("dif:", dif)
        if dif < 1e-6:
            break

        us = copy.deepcopy(us_next)

        t += dt

        if slice_ax == 'x':
            line = []
            for i in range(len(ys)):
                line.append(us[slice_ax_n][i])
            line = ax.plot(ys, line, '-b')
            frames.append(line)
        elif slice_ax == 'y':
            line = []
            for i in range(len(xs)):
                line.append(us[i][slice_ax_n])
            line = ax.plot(xs, line, '-b')
            frames.append(line)

    print('End calc')

    ani = animation.ArtistAnimation(fig, frames, interval=1, blit=True, repeat=True)
    plt.show()


modulation(0, 1, 0, 1)
