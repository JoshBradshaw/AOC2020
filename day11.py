import fileinput
from copy import deepcopy
from itertools import count

def print_grid(grid, label):
    print("-- {} --".format(label))
    print("\n".join(["".join(l).strip() for l in grid]))


def scan(grid, num_rows, num_cols, stop_one):
    directions = [(rd, cd) for rd in range(-1, 2) for cd in range(-1, 2) if rd != 0 or cd != 0]
    seats_to_flip = []

    for row in range(num_rows):
        for col in range(num_cols):
            visible_occupied = 0
            if grid[row][col] in '#L':
                for rd, cd in directions:
                    found = False
                    vr, vc = row + rd, col + cd
                    while -1 < vr < num_rows and -1 < vc < num_cols and not found:
                        if grid[vr][vc] == 'L':
                            found = True
                        if grid[vr][vc] == '#':
                            visible_occupied += 1
                            found = True
                        if stop_one:
                            break

                        vr += rd
                        vc += cd

            if grid[row][col] == 'L' and visible_occupied == 0:
                seats_to_flip.append((row, col))
            if grid[row][col] == '#' and visible_occupied >= 5:
                seats_to_flip.append((row, col))
    return seats_to_flip


def model_seating_arrangements(grid, rule_func):
    num_rows, num_cols = len(grid), len(grid[0])
    seats_to_flip = []
    while True:
        for row, col in seats_to_flip:
            if grid[row][col] == '#':
                grid[row][col] = 'L'
            else:
                grid[row][col] = '#'

        seats_to_flip = rule_func(grid, num_rows, num_cols)

        if not seats_to_flip:
            return sum(row.count('#') for row in grid)


seat_grid = list(map(list, (s.strip() for s in fileinput.input())))
print(model_seating_arrangements(deepcopy(seat_grid), scan))
print(model_seating_arrangements(seat_grid, scan))

