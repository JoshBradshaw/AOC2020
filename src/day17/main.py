"""
If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
"""

import fileinput
import numpy as np

def print_layer3d(gol, input_shape, round, z):
    x_bounds = (gol.shape[0]//2 - input_shape[0]//2 - round, gol.shape[0]//2+input_shape[0]//2 + round+1)
    y_bounds = (gol.shape[1]//2 - input_shape[1]//2 - round, gol.shape[1]//2+input_shape[1]//2 + round+1)

    layer_to_print = gol[x_bounds[0]: x_bounds[1],
                     y_bounds[0]: y_bounds[1],
                     z+gol.shape[2] // 2]

    print('round: {} z: {}'.format(round, z))
    ascii = []
    for row in layer_to_print:
        ascii.append("".join('#' if n else '.' for n in row))
    print('\n'.join(ascii))

def part1(input, n_rounds):
    input = np.array(input)

    l, w = input.shape
    gol = np.zeros((l, w, 1), dtype=bool)
    gol[:, :, 0] = input
    gol = np.pad(gol,
                 ((3 * n_rounds, 3 * n_rounds), (3 * n_rounds, 3 * n_rounds), (3 * n_rounds, 3 * n_rounds)),
                 'constant')

    for round in range(n_rounds):
        #print_layer(gol, input.shape, round, 0)
        next_gol = np.copy(gol)

        xmax = gol.shape[0]
        ymax = gol.shape[1]
        zmax = gol.shape[2]
        for x, y, z in np.ndindex(gol.shape):
            element = gol[x, y, z]
            neighbors = gol[max(0, x-1):min(xmax, x+2), max(0, y-1):min(ymax, y+2), max(0, z-1):min(zmax, z+2)]
            neighbors_sum = np.sum(neighbors) - element
            if element > 0 and 2 <= neighbors_sum <= 3:
                pass
            elif element > 0:
                next_gol[x, y, z] = 0
            elif element == 0 and neighbors_sum == 3:
                next_gol[x, y, z] = 1
            else:
                pass
        gol = next_gol

    return np.sum(gol)

def part2(input, n_rounds):
    input = np.array(input)

    gol = np.zeros((*input.shape, 1, 1), dtype=bool)
    gol[:, :, 0, 0] = input
    gol = np.pad(gol, n_rounds, 'constant')

    for round in range(n_rounds):
        next_gol = np.copy(gol)

        xmax, ymax, zmax, wmax = gol.shape
        for x, y, z, w in np.ndindex(gol.shape):
            element = gol[x, y, z, w]
            neighbors = gol[max(0, x - 1):min(xmax, x + 2),
                            max(0, y - 1):min(ymax, y + 2),
                            max(0, z - 1):min(zmax, z + 2),
                            max(0, w - 1):min(wmax, w + 2)]
            
            neighbors_sum = np.sum(neighbors) - element

            if element > 0 and not 2 <= neighbors_sum <= 3:
                next_gol[x, y, z, w] = 0
            if element == 0 and neighbors_sum == 3:
                next_gol[x, y, z, w] = 1
        gol = next_gol
    return np.sum(gol)


input = []
for line in fileinput.input():
    input.append([int(n) for n in line.strip().replace('#', '1').replace('.', '0')])

print(part1(input, 6))
print(part2(input, 6))