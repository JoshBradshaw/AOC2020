import fileinput
from copy import deepcopy
from itertools import count

def print_grid(seat_grid, label):
    print("-- {} --".format(label))
    print("\n".join(["".join(l).strip() for l in seat_grid]))

def part1(seat_grid):
    num_rows, num_cols = len(seat_grid), len(seat_grid[0])
    num_changes = 1

    while num_changes > 0:
        new_grid = deepcopy(seat_grid)
        num_changes = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if not seat_grid[row][col] in "#L":
                    continue

                adj = [seat_grid[r][c] for r in range(row-1, row+2) for c in range(col-1, col+2)
                       if -1 < r < num_rows and -1 < c < num_cols and (r != row or c != col)]

                if seat_grid[row][col] == 'L' and adj.count('#') == 0:
                    new_grid[row][col] = '#'
                    num_changes += 1
                if seat_grid[row][col] == '#' and adj.count('#') >= 4:
                    new_grid[row][col] = 'L'
                    num_changes += 1
        seat_grid = new_grid
    return sum(row.count('#') for row in seat_grid)

def part2(seat_grid):
    num_rows, num_cols = len(seat_grid), len(seat_grid[0])
    directions = [(rd, cd) for rd in range(-1, 2) for cd in range(-1, 2) if abs(rd) + abs(cd) != 0]
    num_changes = 1

    while num_changes > 0:
        new_grid = deepcopy(seat_grid)
        num_changes = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if not seat_grid[row][col] in '#L':
                    continue

                visible_occupied = 0
                for rd, cd in directions:
                    found = False
                    vr, vc = row + rd, col + cd
                    while -1 < vr < num_rows and -1 < vc < num_cols and not found:
                        if seat_grid[vr][vc] == 'L':
                            found = True
                        if seat_grid[vr][vc] == '#':
                            visible_occupied += 1
                            found = True

                        vr += rd
                        vc += cd

                if seat_grid[row][col] == 'L' and visible_occupied == 0:
                    new_grid[row][col] = '#'
                    num_changes += 1
                if seat_grid[row][col] == '#' and visible_occupied >= 5:
                    new_grid[row][col] = 'L'
                    num_changes += 1
        seat_grid = new_grid
    return sum(row.count('#') for row in seat_grid)


seat_grid = list(map(list, (s.strip() for s in fileinput.input())))
print(part1(seat_grid))
print(part2(seat_grid))

