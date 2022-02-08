import numpy as np
import config


def count_wave():
    count_pure()
    X = config.pixels
    Y = config.wave_lenghts
    X2 = X * X
    XY = X * Y
    k = (XY.mean() - (X.mean()) * (Y.mean())) / (X2.mean() - X.mean() ** 2)
    b = Y.mean() - k * (X.mean())
    config.k = k
    config.b = b

    for i in range(3):
        for j in range(len(config.data[i][0])):
            config.data[i][0][j] = k*config.data[i][0][j] + b


def count_pure():
    for i in range(2):
        config.data[i] = [[], []]
        for j in range(len(config.pltFullData16[i])):
            if j>config.first_norm_pixel:
                config.data[i][0].append(j)
                config.data[i][1].append(config.pltFullData16[i][j])
    if config.to_draw_divided == 1:
        if config.num_divided == 0:
            co_one_two()
        else:
            co_two_one()

def co_one_two():
    config.num_divided = 0
    x = []
    y = []
    ind1 = 0
    ind2 = 0
    cont = True
    while cont:
        if config.data[0][0][ind1] < config.data[1][0][ind2]:
            ind1 += 1
            if ind1 >= len(config.data[0][0]):
                cont = False
        elif config.data[0][0][ind1] > config.data[1][0][ind2]:
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
        else:
            new_y = (1.0 * config.data[0][1][ind1]) / (1.0 * config.data[1][1][ind2])
            if ((1.0 * config.data[1][1][ind2]) >= config.min_intens_value) and (new_y<config.max_intens_div):
                x.append(config.data[0][0][ind1])
                y.append(new_y)
            ind1 += 1
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
            if ind1 >= len(config.data[0][0]):
                cont = False

    config.data[2] = [x, y]
    config.to_draw_divided = 1


def co_two_one():
    config.num_divided = 1
    x = []
    y = []
    ind1 = 0
    ind2 = 0
    cont = True
    while cont:
        if config.data[0][0][ind1] < config.data[1][0][ind2]:
            ind1 += 1
            if ind1 >= len(config.data[0][0]):
                cont = False
        elif config.data[0][0][ind1] > config.data[1][0][ind2]:
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
        else:
            new_y = (1.0 * config.data[1][1][ind2]) / (1.0 * config.data[0][1][ind1])
            if ((1.0 * config.data[0][1][ind1]) >= config.min_intens_value) and (new_y<config.max_intens_div):
                x.append(config.data[0][0][ind1])
                y.append(new_y)
            ind1 += 1
            ind2 += 1
            if ind2 >= len(config.data[1][0]):
                cont = False
            if ind1 >= len(config.data[0][0]):
                cont = False

    config.data[2] = [x, y]
    config.to_draw_divided = 1