import fileinput
from functools import reduce
import math
import numpy as np
import operator
import re
from collections import namedtuple, Counter, defaultdict


Tile = namedtuple('Tile', ['tile_id', 'array'])
TileEdges = namedtuple('Edges', ['top', 'right', 'bottom', 'left'])
TileEdgeLookup = namedtuple('TileWithEdge', ['tile_id', 'edge_orientation'])


def get_edges(tile_array, w):
    def tile_edge_to_str(row):
        return "".join('#' if c else '.' for c in row)

    top_edge = tile_edge_to_str(tile_array[0, :])
    bottom_edge = tile_edge_to_str(np.flip(tile_array[w - 1, :]))
    left_edge = tile_edge_to_str(np.flip(tile_array[:, 0]))
    right_edge = tile_edge_to_str(tile_array[:, w - 1])

    return TileEdges(top_edge, right_edge, bottom_edge, left_edge)


def find_corners(tiles, tile_size):
    edges = {}
    for tile_id, tile_array in tiles.values():
        edges[tile_id] = TileEdges(*get_edges(tile_array, tile_size))


    edges_flattened = []
    for _, edge_list in edges.items():
        edges_flattened.extend([e for e in edge_list])
        edges_flattened.extend([e[::-1] for e in edge_list])

    edge_occurrences = Counter(edges_flattened)

    corner_pieces = []
    for tile_id, tile_array in tiles.values():
        n_edge_matches = sum(edge_occurrences[e] for e in get_edges(tile_array, tile_size))
        if n_edge_matches == 6:
            corner_pieces.append(Tile(tile_id, tile_array))

    # get corner piece and orient it such that it fits in (0, 0) position
    tl_corner = corner_pieces[0]
    while [edge_occurrences[e] for e in get_edges(tl_corner.array, tile_size)] != [1, 2, 2, 1]:
        print([edge_occurrences[e] for e in get_edges(tl_corner.array, tile_size)])
        tl_corner = Tile(tl_corner.tile_id, np.rot90(tl_corner.array))

    return reduce(operator.mul, [c.tile_id for c in corner_pieces]), tl_corner

def assemble_puzzle(tiles, top_left_corner, tile_size, grid_size):
    edge_lookup = defaultdict(list)
    for tile_id, tile_array in tiles.values():
        for edge, edge_name in zip(get_edges(tile_array, tile_size), TileEdges._fields):
            edge_lookup[edge].append(TileEdgeLookup(tile_id, edge_name))

    puzzle = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    puzzle[0][0] = top_left_corner

    def get_child_tile_id(parent_tile_id, edge_to_match):
        is_reversed = False
        for t in edge_lookup[edge_to_match]:
            if t.tile_id != parent_tile_id:
                return t, is_reversed
        is_reversed = True
        for t in edge_lookup[edge_to_match[::-1]]:
            if t.tile_id != parent_tile_id:
                return t, is_reversed

    # fill in top row
    for ii in range(1, grid_size):
        top_tile = puzzle[0][ii-1]

        edges_to_match = get_edges(top_tile.array, tile_size)
        (child_tile_id, child_tile_edge), is_reversed = get_child_tile_id(top_tile.tile_id, edges_to_match.right)

        _, right_child_tile_array = tiles[child_tile_id]
        if child_tile_edge is 'top':
                if not is_reversed:
                    puzzle[0][ii] = Tile(child_tile_id, np.flipud(np.rot90(right_child_tile_array, k=1)))
                else:
                    puzzle[0][ii] = Tile(child_tile_id, np.rot90(right_child_tile_array, k=1))
        elif child_tile_edge is 'right':
            if not is_reversed:
                puzzle[0][ii] = Tile(child_tile_id, np.flipud(np.rot90(right_child_tile_array, k=2)))
            else:
                puzzle[0][ii] = Tile(child_tile_id, np.rot90(right_child_tile_array, k=2))
        elif child_tile_edge is 'bottom':
            if not is_reversed:
                puzzle[0][ii] = Tile(child_tile_id, np.flipud(np.rot90(right_child_tile_array, k=3)))
            else:
                puzzle[0][ii] = Tile(child_tile_id, np.rot90(right_child_tile_array, k=3))
        else:
            if not is_reversed:
                puzzle[0][ii] = Tile(child_tile_id, np.flipud(right_child_tile_array))
            else:
                puzzle[0][ii] = Tile(child_tile_id, right_child_tile_array)

    # fill the rest of the puzzle
    for ii in range(1, grid_size):
        for jj in range(grid_size):
            top_tile = puzzle[ii-1][jj]
            edges_to_match = get_edges(top_tile.array, tile_size)

            (child_tile_id, child_tile_edge), is_reversed = get_child_tile_id(top_tile.tile_id, edges_to_match.bottom)

            _, right_child_tile_array = tiles[child_tile_id]
            if child_tile_edge is 'right':
                if not is_reversed:
                    puzzle[ii][jj] = Tile(child_tile_id, np.fliplr(np.rot90(right_child_tile_array, k=1)))
                else:
                    puzzle[ii][jj] = Tile(child_tile_id, np.rot90(right_child_tile_array, k=1))
            elif child_tile_edge is 'bottom':
                if not is_reversed:
                    puzzle[ii][jj] = Tile(child_tile_id, np.fliplr(np.rot90(right_child_tile_array, k=2)))
                else:
                    puzzle[ii][jj] = Tile(child_tile_id, np.rot90(right_child_tile_array, k=2))
            elif child_tile_edge is 'left':
                if not is_reversed:
                    puzzle[ii][jj] = Tile(child_tile_id, np.fliplr(np.rot90(right_child_tile_array, k=3)))
                else:
                    puzzle[ii][jj] = Tile(child_tile_id, np.rot90(right_child_tile_array, k=3))
            else:
                if not is_reversed:
                    puzzle[ii][jj] = Tile(child_tile_id, np.fliplr(right_child_tile_array))
                else:
                    puzzle[ii][jj] = Tile(child_tile_id, right_child_tile_array)

    return puzzle

def part2(puzzle, tile_size, grid_width):
    image = np.zeros(((tile_size-2) * grid_width, (tile_size - 2) * grid_width), dtype=bool)

    sea_monster = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1],
                            [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0]], dtype=bool)

    for ii, row in enumerate(range(0, grid_width * (tile_size - 2), tile_size - 2)):
        for jj, col in enumerate(range(0, grid_width * (tile_size - 2), tile_size - 2)):
            image[row:row+tile_size-2, col:col+tile_size-2] = puzzle[ii][jj].array[1:tile_size-1, 1:tile_size-1]


    images = [image, np.rot90(image), np.rot90(image, k=2), np.rot90(image, k=3),
                np.fliplr(image), np.rot90(np.fliplr(image)), np.rot90(np.fliplr(image), k=2),
                np.rot90(np.fliplr(image), k=3)]

    n_monsters = []
    for image in images:
        num_monsters_found = 0
        for r, c in np.ndindex(image.shape[0]-sea_monster.shape[0], image.shape[1]-sea_monster.shape[1]):
            if np.sum(np.bitwise_and(image[r:r+sea_monster.shape[0], c:c+sea_monster.shape[1]], sea_monster)) == np.sum(sea_monster):
                num_monsters_found += 1
        n_monsters.append(num_monsters_found)

    return np.sum(image) - np.sum(sea_monster) * max(n_monsters)


def parse(input_stream):
    tiles = {}

    tile_id = ""
    tile = []
    for line in input_stream:
        if "Tile" in line:
            tile_id = int(re.search(r'(\d+)', line).group(1))
        elif not line.strip():
            tiles[tile_id] = Tile(tile_id=tile_id, array=np.array(tile))
            tile = []
        else:
            tile.append(np.array([1 if c == '#' else 0 for c in line.strip()]))

    tiles[tile_id] = Tile(tile_id=tile_id, array=np.array(tile))
    return tiles, len(tile[0])


def print_tile(tile):
    tile_id, array = tile

    print(f"{tile_id}")
    tile_str = []
    for row in array:
        tile_str.append("".join('#' if c else '.' for c in row))
    print('\n'.join(tile_str))


def print_tile_edges(tile_edge):
    top, right, bottom, left = tile_edge

    print(f"top:    {top}")
    print(f"right:   {right}")
    print(f"bottom:  {bottom}")
    print(f"left: {left}")


tiles, tile_size = parse(fileinput.input())
part1_ans, top_left_corner = find_corners(tiles, tile_size)
print(part1_ans)
grid_size = int(math.sqrt(len(tiles)))

puzzle = assemble_puzzle(tiles, top_left_corner, tile_size, grid_size)
print(part2(puzzle, tile_size, grid_size))