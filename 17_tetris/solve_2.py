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
    need_total = len(rock) + need_free_space
    diff = need_total - count_free_space()

    if diff < 0:
        for _ in range(-diff):
            field.pop()
    else:
        for _ in range(diff):
            field.append(['.'] * field_width)


def count_before_flat():
    count = 0

    for line in reversed(field):
        if all(c == '#' for c in line):
            break
        else:
            count += 1

    return count - count_free_space()


def display_field():
    print('\n'.join(''.join(line) for line in reversed(field)))
    print()


with open('input.txt') as f:
    move_patterns = f.read().strip()

with open('rock_patterns.txt') as f:
    rock_patterns = f.read().split('\n\n')

rock_patterns = [[list(line) for line in rock_pattern.strip().split('\n')] for rock_pattern in rock_patterns]

rock_stream = itertools.cycle(enumerate(rock_patterns))
move_stream = itertools.cycle(enumerate(move_patterns))

field_width = 7
need_free_space = 3

field = []
saw_configurations = dict()
max_steps = 40000
need_total_steps = 1000000000000

result = 0
step_when_to_stop = None
length_when_matched = None

for step in range(max_steps):
    rock_i, rock = next(rock_stream)

    guarantee_enough_space(rock)

    x = 2
    y = 0

    move_i, move = next(move_stream)

    if step == step_when_to_stop:
        print('step at the end =', step)
        result += count_length() - length_when_matched
        break

    if count_before_flat() == 0 and step > 0 and step_when_to_stop is None:
        configuration = rock_i, move_i

        if configuration in saw_configurations:
            cur_length = count_length()
            last_length, last_step = saw_configurations[configuration]

            total_steps_left = need_total_steps - step

            repeatable_length = cur_length - last_length
            repeat_steps_count = step - last_step
            repeats_count = total_steps_left // repeat_steps_count

            result += cur_length
            result += repeatable_length * repeats_count

            step_when_to_stop = step + total_steps_left % repeat_steps_count
            length_when_matched = cur_length

        saw_configurations[configuration] = count_length(), step
        print(saw_configurations)

    while True:
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

        move_i, move = next(move_stream)

print(result)

