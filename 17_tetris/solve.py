import itertools

from pprint import pprint


def can_place(x: int, y: int, rock: list[list[str]]) -> bool:
    for rock_y, line in enumerate(rock):
        for rock_x, c in enumerate(line):
            field_x = x + rock_x
            field_y = len(field) - 1 - y - rock_y

            if not (0 <= field_y < len(field)) or not (0 <= field_x < len(field[field_y])) or (c == '#' and field[field_y][field_x] == '#'):
                return False

    return True


def place(x: int, y: int, rock: list[list[str]]):
    for rock_y, line in enumerate(rock):
        for rock_x, c in enumerate(line):
            field_x = x + rock_x
            field_y = len(field) - 1 - y - rock_y

            assert 0 <= field_y < len(field)
            assert 0 <= field_x < len(field[field_y])

            if c == '#':
                field[field_y][field_x] = c


def count_length() -> int:
    return sum(any(c == '#' for c in line) for line in field)


def count_free_space() -> int:
    return len(field) - count_length()


def guarantee_enough_space(rock: list[list[str]]):
    need_total = len(rock) + 3
    diff = need_total - count_free_space()

    if diff < 0:
        for _ in range(-diff):
            field.pop()
    else:
        for _ in range(diff):
            field.append(['.'] * field_width)


def display_field():
    print('\n'.join(''.join(line) for line in reversed(field)))
    print()


with open('input.txt') as f:
    move_patterns = f.read().strip()

with open('rock_patterns.txt') as f:
    rock_patterns = f.read().split('\n\n')

rock_patterns = [[list(line) for line in rock_pattern.strip().split('\n')] for rock_pattern in rock_patterns]

rock_stream = itertools.cycle(rock_patterns)
move_stream = itertools.cycle(move_patterns)

field_width = 7
need_free_space = 3

field = []

for _ in range(2022):
    rock = next(rock_stream)

    guarantee_enough_space(rock)

    x = 2
    y = 0

    while True:
        move = next(move_stream)

        if move == '<':
            new_x = x - 1
        else:
            new_x = x + 1

        if can_place(new_x, y, rock):
            x = new_x

        new_y = y + 1

        if can_place(x, new_y, rock):
            y = new_y
        else:
            place(x, y, rock)
            break

print(count_length())

