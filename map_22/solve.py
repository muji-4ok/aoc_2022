import re

from enum import Enum
from typing import Optional
from functools import cache


class Tile(Enum):
    Open = '.'
    Wall = '#'


def rc_to_xy(row: int, col: int) -> (int, int):
    y = row
    x = min(t[0] for t in tiles.keys() if t[1] == y) + col
    return x, y


def xy_to_rc(x: int, y: int) -> (int, int):
    row = y
    min_x_in_row = min(t[0] for t in tiles.keys() if t[1] == y)
    col = x - min_x_in_row
    return row, col


@cache
def bounds_at(x: int, y: int) -> (int, int, int, int):
    xs = [t[0] for t in tiles.keys() if t[1] == y]
    ys = [t[1] for t in tiles.keys() if t[0] == x]
    return min(xs), max(xs), min(ys), max(ys)


def try_move(x: int, y: int, direction: (int, int)) -> Optional[tuple[int, int]]:
    new_x = x + direction[0]
    new_y = y + direction[1]

    if (new_x, new_y) not in tiles:
        min_x, max_x, min_y, max_y = bounds_at(x, y)

        if new_x > max_x:
            new_x = min_x

        if new_x < min_x:
            new_x = max_x

        if new_y > max_y:
            new_y = min_y

        if new_y < min_y:
            new_y = max_y

    new_xy = new_x, new_y

    return new_xy if tiles[new_xy] == Tile.Open.value else None


# R, D, L, U
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

with open('input.txt') as f:
    tiles, moves = f.read().split('\n\n')

tiles_lines = tiles.split('\n')

tiles = {}

for y, line in enumerate(tiles_lines):
    for x, c in enumerate(line):
        if c in [e.value for e in Tile]:
            tiles[(x, y)] = c

moves = moves.strip()
moves = re.findall('[LR]|\d+', moves)

direction_i = 0
x, y = rc_to_xy(0, 0)

for move in moves:
    if move == 'R':
        direction_i = (direction_i + 1) % len(directions)
    elif move == 'L':
        direction_i = (direction_i - 1) % len(directions)
    else:
        count = int(move)

        for _ in range(count):
            new_xy = try_move(x, y, directions[direction_i])

            if new_xy is not None:
                x, y = new_xy
            else:
                break

row, col = xy_to_rc(x, y)
row += 1
col += 1

result = 1000 * row + 4 * col + direction_i

print(result)

