import re
import os
import curses
import time

from enum import Enum, Flag, auto
from typing import Optional
from functools import cache
from pprint import pprint
from collections import defaultdict


class Tile(Enum):
    OPEN = '.'
    WALL = '#'


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)

    def to_string(self):
        to_string_dict = {
            RIGHT: '>',
            DOWN: 'v',
            LEFT: '<',
            UP: '^',
        }

        return to_string_dict[self]


RIGHT = Direction.RIGHT
DOWN = Direction.DOWN
LEFT = Direction.LEFT
UP = Direction.UP


class CubeMoveFlags(Flag):
    NONE = 0
    FLIP_XY = auto()
    MIRROR_X = auto()
    MIRROR_Y = auto()


FLIP_XY = CubeMoveFlags.FLIP_XY
MIRROR_X = CubeMoveFlags.MIRROR_X
MIRROR_Y = CubeMoveFlags.MIRROR_Y


def rc_to_xy(row: int, col: int) -> (int, int):
    y = row
    x = min(t[0] for t in tiles.keys() if t[1] == y) + col
    return x, y


def xy_to_rc(x: int, y: int) -> (int, int):
    row = y
    min_x_in_row = min(t[0] for t in tiles.keys() if t[1] == y)
    col = x - min_x_in_row
    return row, col


def make_coord_func(destination_direction: Direction, flags: CubeMoveFlags):
    fixed = {}

    if destination_direction == DOWN:
        fixed['y'] = 0
    elif destination_direction == UP:
        fixed['y'] = side_size - 1
    elif destination_direction == RIGHT:
        fixed['x'] = 0
    else:
        fixed['x'] = side_size - 1

    def mirror_x(func):
        def f(x, y):
            x, y = func(x, y)
            return side_size - x - 1, y

        return f

    def mirror_y(func):
        def f(x, y):
            x, y = func(x, y)
            return x, side_size - y - 1

        return f

    def fix_coord(func, coord_name, coord_value):
        if coord_name == 'x':
            def f(x, y):
                return coord_value, func(x, y)[1]
        else:
            def f(x, y):
                return func(x, y)[0], coord_value

        return f

    if FLIP_XY in flags:
        func = lambda x, y: (y, x)
    else:
        func = lambda x, y: (x, y)

    if MIRROR_X in flags:
        func = mirror_x(func)

    if MIRROR_Y in flags:
        func = mirror_y(func)

    if 'x' in fixed:
        func = fix_coord(func, 'x', fixed['x'])
    else:
        func = fix_coord(func, 'y', fixed['y'])

    return func, destination_direction.value


def try_move(x: int, y: int, direction: (int, int)) -> Optional[tuple[tuple[int, int], tuple[int, int]]]:
    new_x = x + direction[0]
    new_y = y + direction[1]
    new_direction = direction

    if (new_x, new_y) not in tiles:
        cube_x = x // side_size
        cube_y = y // side_size

        (new_cube_x, new_cube_y), cube_coord_func, new_direction = cube_connections[((cube_x, cube_y), direction)]

        x_in_side, y_in_side = cube_coord_func(new_x % side_size, new_y % side_size)
        new_x = new_cube_x * side_size + x_in_side
        new_y = new_cube_y * side_size + y_in_side

    new_xy = new_x, new_y

    return (new_xy, new_direction) if tiles[new_xy] == Tile.OPEN.value else None


def display_path(moved_in: list[tuple[tuple[int, int], tuple[int, int]]]):
    xs = set(t[0] for t in tiles.keys())
    ys = set(t[1] for t in tiles.keys())
    width = len(xs)
    height = len(ys)

    lines = [[' ' for j in range(width)] for i in range(height)]

    for (x, y), tile in tiles.items():
        lines[y][x] = tile

    for (x, y), direction in moved_in:
        lines[y][x] = Direction(direction).to_string()

    return '\n'.join(''.join(line) for line in lines)


directions = [RIGHT.value, DOWN.value, LEFT.value, UP.value]

with open('input.txt') as f:
    tiles, moves = f.read().split('\n\n')

tiles_lines = tiles.split('\n')

tiles = {}

for y, line in enumerate(tiles_lines):
    for x, c in enumerate(line):
        if c in [e.value for e in Tile]:
            tiles[(x, y)] = c

cube_sides = defaultdict(set)
side_size = 50

for x, y in tiles.keys():
    cube_sides[(x // side_size, y // side_size)].add((x, y))

# cube_connections = {
#     ((2, 0), RIGHT.value): ((3, 2), *make_coord_func(LEFT, MIRROR_Y)),
#     ((2, 0), LEFT.value): ((1, 1), *make_coord_func(DOWN, FLIP_XY)),
#     ((2, 0), UP.value): ((0, 1), *make_coord_func(DOWN, MIRROR_X)),
#
#     ((0, 1), DOWN.value): ((2, 2), *make_coord_func(UP, MIRROR_X)),
#     ((0, 1), LEFT.value): ((3, 2), *make_coord_func(UP, MIRROR_X | FLIP_XY)),
#     ((0, 1), UP.value): ((2, 0), *make_coord_func(DOWN, MIRROR_X)),
#
#     ((1, 1), DOWN.value): ((2, 2), *make_coord_func(RIGHT, MIRROR_Y | FLIP_XY)),
#     ((1, 1), UP.value): ((2, 0), *make_coord_func(RIGHT, FLIP_XY)),
#
#     ((3, 2), RIGHT.value): ((2, 0), *make_coord_func(LEFT, MIRROR_Y)),
#     ((3, 2), DOWN.value): ((0, 1), *make_coord_func(RIGHT, MIRROR_Y | FLIP_XY)),
#     ((3, 2), UP.value): ((2, 1), *make_coord_func(LEFT, MIRROR_Y | FLIP_XY)),
#
#     ((2, 2), DOWN.value): ((0, 1), *make_coord_func(UP, MIRROR_X)),
#     ((2, 2), LEFT.value): ((1, 1), *make_coord_func(UP, FLIP_XY)),
#
#     ((2, 1), RIGHT.value): ((3, 2), *make_coord_func(DOWN, MIRROR_X | FLIP_XY)),
# }

cube_connections = {
    ((2, 0), RIGHT.value): ((1, 2), *make_coord_func(LEFT, MIRROR_Y)),
    ((2, 0), DOWN.value): ((1, 1), *make_coord_func(LEFT, FLIP_XY)),
    ((2, 0), UP.value): ((0, 3), *make_coord_func(UP, CubeMoveFlags.NONE)),

    ((0, 3), RIGHT.value): ((1, 2), *make_coord_func(UP, FLIP_XY)),
    ((0, 3), DOWN.value): ((2, 0), *make_coord_func(DOWN, CubeMoveFlags.NONE)),
    ((0, 3), LEFT.value): ((1, 0), *make_coord_func(DOWN, FLIP_XY)),

    ((1, 0), LEFT.value): ((0, 2), *make_coord_func(RIGHT, MIRROR_Y)),
    ((1, 0), UP.value): ((0, 3), *make_coord_func(RIGHT, FLIP_XY)),

    ((0, 2), LEFT.value): ((1, 0), *make_coord_func(RIGHT, MIRROR_Y)),
    ((0, 2), UP.value): ((1, 1), *make_coord_func(RIGHT, FLIP_XY)),

    ((1, 2), RIGHT.value): ((2, 0), *make_coord_func(LEFT, MIRROR_Y)),
    ((1, 2), DOWN.value): ((0, 3), *make_coord_func(LEFT, FLIP_XY)),

    ((1, 1), RIGHT.value): ((2, 0), *make_coord_func(UP, FLIP_XY)),
    ((1, 1), LEFT.value): ((0, 2), *make_coord_func(DOWN, FLIP_XY)),
}

moves = moves.strip()
moves = re.findall('[LR]|\d+', moves)

direction = directions[0]
x, y = rc_to_xy(0, 0)

moved_in = [((x, y), direction)]

for move in moves:
    if move == 'R':
        direction = directions[(directions.index(direction) + 1) % len(directions)]
    elif move == 'L':
        direction = directions[(directions.index(direction) - 1) % len(directions)]
    else:
        count = int(move)

        for _ in range(count):
            result = try_move(x, y, direction)

            if result is not None:
                (x, y), direction = result
                moved_in.append(((x, y), direction))
            else:
                break

row, col = xy_to_rc(x, y)
row += 1
col += 1

print(row, col, directions.index(direction))

result = 1000 * row + 4 * col + directions.index(direction)

print(result)

steps = 1
start_line = 0
total_lines = len(display_path([]).split('\n'))

win = curses.initscr()

try:
    height, width = win.getmaxyx()

    while True:
        win.clear()
        win.addstr(0, 0, f'steps = {steps}')

        max_lines = height - 2
        lines = display_path(moved_in[:steps]).split('\n')[start_line:start_line + max_lines]

        win.addstr(1, 0, '\n'.join(lines))

        win.addstr(height - 1, 0, '> ')

        while True:
            ch = win.getch()

            if ch in range(32, 127):
                break

        command = chr(ch)

        if command == 'n':
            steps += 1
        elif command == 'p':
            steps -= 1
        elif command == 'w':
            start_line -= 1
        elif command == 's':
            start_line += 1
        else:
            win.addstr(height - 1, 5, 'don\'t know')

        steps = max(0, min(steps, len(moved_in)))
        start_line = max(0, min(start_line, total_lines - (height - 2)))

        time.sleep(0.01)
finally:
    curses.endwin()

