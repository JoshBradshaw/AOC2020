from copy import copy
from collections import defaultdict
import fileinput
import re

def part1(directions):
    directions_to_axial_coordinates = {'e': (1, 0), 'w': (-1, 0),
                                       'ne': (1, -1), 'sw': (-1, 1),
                                       'se': (0, 1), 'nw': (0, -1)}
    tile_state = {}

    for direction_list in directions:
        tile_q, tile_r = 0, 0
        for d in direction_list:
            q, r = directions_to_axial_coordinates[d]
            tile_q += q
            tile_r += r

        tile_position = (tile_q, tile_r)
        if tile_position not in tile_state:
            tile_state[tile_position] = True
        else:
            tile_state[tile_position] = not tile_state[tile_position]

    return sum(t for t in tile_state.values()), set(tile_pos for tile_pos, state in tile_state.items() if state)


def part2(active_tile_set, n_iterations):
    neighbor_sq = [(1, 0), (-1, 0), (1, -1), (-1, 1), (0, 1), (0, -1)]

    for _ in range(n_iterations):
        black_neighbor_count = defaultdict(lambda: 0)

        for tile_pos in active_tile_set:
            if tile_pos not in black_neighbor_count:
                black_neighbor_count[tile_pos] = 0

            for ns, nq in neighbor_sq:
                tile_s, tile_q = tile_pos
                black_neighbor_count[(tile_s+ns, tile_q+nq)] += 1

        tmp_active_tile_set = copy(active_tile_set)
        for tile_pos, count in black_neighbor_count.items():
            if (count == 0 or count > 2) and tile_pos in tmp_active_tile_set:
                active_tile_set.remove(tile_pos)
            if count == 2 and tile_pos not in tmp_active_tile_set:
                active_tile_set.add(tile_pos)

    return len(active_tile_set)


directions = []
for line in fileinput.input():
    direction_regex = re.compile(r'(se|sw|nw|ne|w|e)')
    directions.append(direction_regex.findall(line))

part1_answer, part2_initial_state = part1(directions)
print(part1_answer)
print(part2(part2_initial_state, 100))

